from round_fountion_truncated import *
from gurobipy import *


class joltik_boom():
    def __init__(self, keysize):
        assert keysize == 128 or keysize == 192
        self.s = int(keysize / 64)
        self.keysize = keysize

    def gen_Objective(self, R):
        f = ''
        for i in range(0, R[0]):
            x = genVars_InVars_at_Round('up_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        for i in range(0, R[1]):
            x = genVars_InVars_at_Round('mi_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        for i in range(R[1], R[1] + R[2]):
            x = genVars_InVars_at_Round('lo_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        return f[3:]

    def gen_constraints(self, i):
        constraints = list()
        x = ['up_x_0_' + str(i) for i in range(16)]
        constraints = constraints + [' + '.join(x) + ' <= 8']

        x = ['lo_x_' + str(i) + '_' + str(j) for j in range(16)]
        constraints = constraints + [' + '.join(x) + ' <= 4']

        LANE = ['lo_LANE' + '_' + str(i) for i in range(16)]
        constraints = constraints + [' + '.join(LANE) + ' <= 2']

        return constraints

    def genConstraints_init(self, path, r):
        constraints = list()

        LANE = [path + '_LANE' + '_' + str(i) for i in range(16)]
        constraints = constraints + [' + '.join(LANE) + ' >= 1']
        x = [path + '_x' + '_' + str(r) + '_' + str(j) for j in range(16)]
        constraints = constraints + [ ' + '.join(x) + ' <= 4']

        return constraints

    def genConstraints_outer_Round(self, path, r):
        assert r >= 0
        constraints = list()

        X0 = genVars_InVars_at_Round(path + '_x', r, 16)
        t = SR(X0)

        Y = genVars_InVars_at_Round(path + '_y', r, 16)
        d = genVars_InVars_at_Round(path + '_d', r, 4)
        constraints = constraints + MN(t, Y, d)

        STK = genVars_InVars_at_Round(path + '_stk', r, 16)
        X1 = genVars_InVars_at_Round(path + '_x', r + 1, 16)
        constraints = constraints + ART(Y, STK, X1)

        c = genVars_InVars_at_Round(path + '_c', r, 16)
        constraints = constraints + ART_c(Y, STK, X1, c)

        TYPE = genVars_InVars_at_Round(path + '_TYPE', r, 4)
        for i in range(4):
            f1 = []
            f2 = []
            f3 = []
            for j in range(4):
                f1.append(Y[4 * i + j])
                f2.append(c[4 * i + j])
                f3.append(t[4 * i + j])
            f1 = ' + '.join(f1)
            f2 = ' - '.join(f2)
            f3 = ' + '.join(f3)
            constraints = constraints + [TYPE[i] + ' - 4 ' + d[i] + ' + ' + f1 + ' - ' + f2 + ' + ' + f3 + ' >= 0 ']
            constraints = constraints + [TYPE[i] + ' >= 0']
        return constraints

    def genConstraints_inner_Round(self, path, r):
        assert r >= 0
        constraints = list()

        X0 = genVars_InVars_at_Round(path + '_x', r, 16)
        t = SR(X0)

        d = genVars_InVars_at_Round(path + '_d', r, 4)
        Y = genVars_InVars_at_Round(path + '_y', r, 16)
        constraints = constraints + MN(t, Y, d)

        STK = genVars_InVars_at_Round(path + '_stk', r, 16)
        X1 = genVars_InVars_at_Round(path + '_x', r + 1, 16)
        if path == 'up':
            constraints = constraints + ART_inner(Y, STK, X1)
        else:
            constraints = constraints + ART_inner(X1, STK, Y)

        TYPE = genVars_InVars_at_Round(path + '_TYPE', r, 4)
        for i in range(4):
            f1 = []
            f2 = []
            for j in range(4):
                f1.append(Y[4 * i + j])
                f2.append(t[4 * i + j])
            f1 = ' + '.join(f1)
            f2 = ' + '.join(f2)
            constraints = constraints + [TYPE[i] + ' - 4 ' + d[i] + ' + ' + f1 + ' + ' + f2 + ' >= 0 ']
            constraints = constraints + [TYPE[i] + ' >= 0']

        return constraints

    def genConstraints_additional(self, path, R):
        if path == 'up':
            r = R[0]
        else:
            r = R[2]
        rm = R[1]

        constraints = list()
        LANE = [path + '_LANE' + '_' + str(j) for j in range(16)]
        f1 = str(self.s) + ' ' + (' + ' + str(self.s) + ' ').join(LANE)
        f1 = f1 + ' - ' + str(r + rm) + ' ' + (' - ' + str(r + rm) + ' ').join(LANE)
        #        print(f1)

        STK = [None] * (r + rm)
        f2 = ''
        for i in range(16):
            for j in range(r + rm):
                STK[j] = genVars_InVars_at_Round(path + '_stk', j, 16)
                if i == 0: f2 = f2 + ' + ' + ' + '.join(STK[j])
                for k in range(j):
                    STK[j] = h(STK[j])
        constraints = constraints + key_shedule(LANE, STK, r + rm, self.s)
        #        print(f2)

        f3 = ''
        for i in range(r + rm):
            TYPE = genVars_InVars_at_Round(path + '_TYPE', i, 4)
            f3 = f3 + ' - ' + ' - '.join(TYPE)
        #        print(f3)

        constraints = constraints + [f1 + f2 + f3 + ' >= 0']

        return constraints

    def genConstraints_middle(self, R):
        constraints = list()
        for  i in range(R[1]):
            y = ['mi_x_' + str(i) + '_' + str(j) for j in range(16)]
            y1 = ['up_x_' + str(R[0] + i) + '_' + str(j) for j in range(16)]
            y2 = ['lo_x_' + str(i) + '_' + str(j) for j in range(16)]
            constraints = constraints + middle_constraints(y1, y2, y)

        return constraints

    def gen_wrongtrail(self, R):
        constraints = list()
        PATH = f'wrong trail/{R[0]}, {R[1]}, {R[2]}'
        if os.path.exists(PATH) == 0:
            os.mkdir(PATH)


        PATH_list = os.listdir(PATH)
        obj = []
        for name in PATH_list:
            with open(PATH + '/' + name, 'r') as f:
                temp = f.readlines()

                a = temp[:1][0][:-1]
                i = -1
                while a[i] != ' ': i = i - 1
                obj.append(int(a[i + 1:]))

                C = []
                for line in temp[1:]:
                    if line[3: 4] == 'x' and int(line[-2: -1]) == 1:
                        C.append(line[:-3])
                a = ''
                sum = 0
                for i in range(R[0]):
                    for j in range(16):
                        v = 'up_x_' + str(i) + '_' + str(j)
                        if v in C:
                            sum = sum + 1
                            a = a + " - " + v
                        else:
                            a = a + ' + ' + v
                for i in range(R[1]):
                    for j in range(16):
                        v = 'mi_x_' + str(i) + '_' + str(j)
                        if v in C:
                            sum = sum + 1
                            a = a + " - " + v
                        else:
                            a = a + ' + ' + v
                for i in range(R[1], R[1] + R[2]):
                    for j in range(16):
                        v = 'lo_x_' + str(i) + '_' + str(j)
                        if v in C:
                            sum = sum + 1
                            a = a + " - " + v
                        else:
                            a = a + ' + ' + v
                constraints = constraints + [a[1:] + " >= " + str(1 - sum)]
        if len(obj) > 0:
            constraints = constraints + [self.gen_Objective(R) + ' >= ' + str(max(obj))]
        return constraints

    def genModel_trunc(self, C, r):

        C = C + self.gen_constraints(r[1] + r[2])

        C = C + self.genConstraints_init('up', r[0])
        for i in range(0, r[0]):
            C = C + self.genConstraints_outer_Round('up', i)
        for i in range(r[0], r[0] + r[1]):
            C = C + self.genConstraints_inner_Round('up', i)
        C = C + self.genConstraints_additional('up', r)

        C = C + self.genConstraints_init('lo', r[1] - 1)
        for i in range(0, r[1]):
            C = C + self.genConstraints_inner_Round('lo', i)
        for i in range(r[1], r[1] + r[2]):
            C = C + self.genConstraints_outer_Round('lo', i)
        C = C + self.genConstraints_additional('lo', r)

        C = C + self.genConstraints_middle(r)

        C = C + self.gen_wrongtrail(r)

        V1 = getVariables_binary_Constraints(C)
        V2 = getVariables_integer_Constraints(C)

        filename = 'joltik' + str(self.keysize) + '_boom_' + f'({r[0]}, {r[1]}, {r[2]})' + '.lp'
        o = open(filename, 'w')

        o.write('Minimize\n')
        o.write(self.gen_Objective(r))
        o.write('\n\n')

        o.write('Subject To\n')
        for c in C:
            o.write(c)
            o.write('\n')
        o.write('\n\n')

        o.write('Binary\n')
        for v in V1:
            o.write(v)
            o.write('\n')

        o.write('\nInteger\n')
        for v in V2:
            o.write(v)
            o.write('\n')
        o.close()


if __name__ == '__main__':
    print('Initialized...')
    r = [3, 2, 3]
    keysize = 128

    constraints = list([])
    m = joltik_boom(keysize)

    m.genModel_trunc(constraints, r)
    m = read("joltik" + str(keysize) + "_boom_" + f'({r[0]}, {r[1]}, {r[2]})' + ".lp")
    m.optimize()
#    for v in m.getVars():
#        print(v.varName, v.x)

    m.write("joltik" + str(keysize) + "_boom_" + f'({r[0]}, {r[1]}, {r[2]})' + ".sol")
