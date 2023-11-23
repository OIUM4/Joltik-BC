from round_fountion_truncated import *
from gurobipy import *

class joltik_boom():
    def __init__(self, keysize):
        assert keysize == 128 or keysize == 192
        self.s = int(keysize / 64)
        self.keysize = keysize

    def gen_Objective(self, R):
        f = ''
        for i in range(R[0], R[0] + R[1]):
            x = genVars_InVars_at_Round('up_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        for i in range(0, R[2]):
            x = genVars_InVars_at_Round('mi_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        for i in range(R[2], R[2] + R[3]):
            x = genVars_InVars_at_Round('lo_x', i, 16)
            f = f + ' + ' + ' + '.join(x)
        return f[3:]

    def genConstraints_init(self, r):
        constraints = list()
        x = genVars_InVars_at_Round('up_x', 0, 16)
        constraints = constraints + [' + '.join(x) + ' <= 4']

        x = genVars_InVars_at_Round('lo_x', r[2] + r[3] + r[4] - 1, 16)
        constraints = constraints + [' + '.join(x) + ' <= 6']

        return constraints

    def genConstraints_normal_Round(self, path, r):
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

    def genConstraints_forward_Round(self, path, r):
        assert r >= 0
        constraints = list()

        X0 = genVars_InVars_at_Round(path + '_x', r + 1, 16)
        STK = genVars_InVars_at_Round(path + '_stk', r, 16)
        Y = genVars_InVars_at_Round(path + '_y', r, 16)
        constraints = constraints + ART_inner(X0, STK, Y)

        X1 = genVars_InVars_at_Round(path + '_x', r, 16)
        t = SR(X1)
        if path == 'up':
            constraints = constraints + MN_out(Y, t)
        else:
            d = genVars_InVars_at_Round(path + '_d', r, 4)
            constraints = constraints + MN(Y, t, d)

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

    def genConstraints_backward_Round(self, path, r):
        assert r >= 0
        constraints = list()

        X1 = genVars_InVars_at_Round(path + '_x', r + 1, 16)

        STK = genVars_InVars_at_Round(path + '_stk', r, 16)
        Y = genVars_InVars_at_Round(path + '_y', r, 16)
        constraints = constraints + ART_inner(Y, STK, X1)

        X0 = genVars_InVars_at_Round(path + '_x', r, 16)
        t = SR(X0)
        if path == 'lo':
            constraints = constraints + MN_out(t, Y)
        else:
            d = genVars_InVars_at_Round(path + '_d', r, 4)
            constraints = constraints + MN(t, Y, d)

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

    def genConstraints_keyshedule(self, path, R):
        if path == 'up':
            r1 = R[0] + R[1]
            if R[0] >= 1: r2 = R[1] + 1
            else: r2 = R[1]
        else:
            r1 = R[3] + R[4]
            r2 = R[3]
        rm = R[2]

        constraints = list()
        LANE = [path + '_LANE' + '_' + str(j) for j in range(16)]
        constraints = constraints + [' + '.join(LANE) + ' >= 1']

        f1 = str(self.s) + ' ' + (' + ' + str(self.s) + ' ').join(LANE)
        f1 = f1 + ' - ' + str(r2 + rm) + ' ' + (' - ' + str(r2 + rm) + ' ').join(LANE)
        #        print(f1)

        STK = [None] * (r1 + rm)
        f2 = ''
        for i in range(16):
            for j in range(r1 + rm):
                STK[j] = genVars_InVars_at_Round(path + '_stk', j, 16)
                if path == 'up':
                    if i == 0 and  j >= r1 -r2 : f2 = f2 + ' + ' + ' + '.join(STK[j])
                else:
                    if i == 0 and j <= r2 + rm - 1: f2 = f2 + ' + ' + ' + '.join(STK[j])
                for k in range(j):
                    STK[j] = h(STK[j])
        constraints = constraints + key_shedule(LANE, STK, r1 + rm, self.s)
        #        print(f2)

        f3 = ''
        if path == 'up':
            for i in range(r1 - r2, r1 + rm):
                TYPE = genVars_InVars_at_Round(path + '_TYPE', i, 4)
                f3 = f3 + ' - ' + ' - '.join(TYPE)
        else:
            for i in range(0, r2 + rm):
                TYPE = genVars_InVars_at_Round(path + '_TYPE', i, 4)
                f3 = f3 + ' - ' + ' - '.join(TYPE)
        #        print(f3)

        constraints = constraints + [f1 + f2 + f3 + ' >= 0']

        return constraints

    def genConstraints_middle(self, R):
        constraints = list()
        for i in range(R[2]):
            y = ['mi_x_' + str(i) + '_' + str(j) for j in range(16)]
            y1 = ['up_x_' + str(R[0] + R[1] + i) + '_' + str(j) for j in range(16)]
            y2 = ['lo_x_' + str(i) + '_' + str(j) for j in range(16)]
            constraints = constraints + middle_constraints(y1, y2, y)

        return constraints

    def genModel_trunc(self, C, r):
        assert r[2] >= 1

        C = C + self.genConstraints_init(r)

        '''UPPER TRUNCATED TRAIL'''
        if r[0] == 0:
            for i in range(0, r[1]):
                C = C + self.genConstraints_normal_Round('up', i)
        else:
            for i in range(0, r[0] - 1):
                C = C + self.genConstraints_forward_Round('up', i)
            for i in range(r[0] - 1, r[0] + r[1]):
                C = C + self.genConstraints_normal_Round('up', i)
        for i in range(r[0] + r[1], r[0] + r[1] + r[2]):
            C = C + self.genConstraints_backward_Round('up', i)
        C = C + self.genConstraints_keyshedule('up', r)

        '''LOWWER TRUNCATED TRAIL'''
        for i in range(0, r[2] - 1):
            C = C + self.genConstraints_forward_Round('lo', i)
        for i in range(r[2] - 1, r[2] + r[3]):
            C = C + self.genConstraints_normal_Round('lo', i)
        for i in range(r[2] + r[3], r[2] + r[3] + r[4]):
            C = C + self.genConstraints_backward_Round('lo', i)
        C = C + self.genConstraints_keyshedule('lo', r)

        C = C + self.genConstraints_middle(r)

        # C = C + self.gen_wrongtrail(r)

        V1 = getVariables_binary_Constraints(C)
        V2 = getVariables_integer_Constraints(C)

        filename = 'joltik' + str(self.keysize) + '_boom_' + f'({r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]})' + '.lp'
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
    r = [2, 4, 3, 3, 1]
    keysize = 128

    constraints = list([])
    m = joltik_boom(keysize)
    m.genModel_trunc(constraints, r)
    m = read("joltik" + str(keysize) + "_boom_" + f'({r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]})' + ".lp")
    m.optimize()
#    for v in m.getVars():
#        print(v.varName, v.x)

    m.write("joltik" + str(keysize) + "_boom_" + f'({r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]})' + ".sol")
