from round_fountion_truncated import *
from gurobipy import *

class joltik_boom():
    def __init__(self, keysize):
        assert keysize == 128 or keysize == 192
        self.s = int(keysize / 64)
        self.keysize = keysize

    def gen_Objective(self, r) :
        assert r >= 0
        f = ''
        for i in range(1, r):
            y = genVars_InVars_at_Round('x', i, 16)
            f = f + ' + ' + ' + '.join(y)
        return f[3:]

    def genConstraints_init(self, r):
        constraints = list()
        LANE = ['LANE_' + str(j) for j in range(16)]
        constraints = constraints + [' + '.join(LANE) + ' >= 1']
        X = genVars_InVars_at_Round('x', 0, 16)
        constraints = constraints + [' + '.join(X) + ' <= 4']

        constraints = constraints + [f'x_{r}_1 = 0'] + [f'x_{r}_6 = 0'] + [f'x_{r}_11 = 0'] + [f'x_{r}_12 = 0']


        return constraints

    def genConstraints_of_Round(self, r):
        assert r>=0
        constraints = list()

        X0 = genVars_InVars_at_Round('x', r, 16)
        t =SR(X0)

        Y = genVars_InVars_at_Round('y', r, 16)
        d = genVars_InVars_at_Round('d', r, 4)
        constraints = constraints + MN(t, Y, d)

        STK = genVars_InVars_at_Round('stk', r, 16)
        X1 = genVars_InVars_at_Round('x', r + 1, 16)
        constraints = constraints + ART(Y, STK, X1)

        c = genVars_InVars_at_Round('c', r, 16)
        constraints = constraints + ART_c(Y, STK, X1, c)

        TYPE = genVars_InVars_at_Round('TYPE', r, 4)
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

    def genConstraints_additional(self, r):
        assert  r>=0

        constraints = list()
        LANE = ['LANE_' + str(j) for j in range(16)]
        f1 = str(self.s) + ' ' + (' + '+ str(self.s) + ' ').join(LANE)
        f1 = f1 + ' - ' + str(r) + ' ' + (' - ' + str(r) + ' ').join(LANE)
#        print(f1)

        STK = [None] * r
        f2 = ''
        for i in range(16):
            for j in range(r):
                STK[j] = genVars_InVars_at_Round('stk', j, 16)
                if i == 0 : f2 = f2 + ' + ' +' + '.join(STK[j])
                for k in range(j):
                    STK[j] = h(STK[j])
        constraints = constraints + key_shedule(LANE, STK, r, self.s)
#        print(f2)

        f3 = ''
        for i in range(r):
            TYPE = genVars_InVars_at_Round('TYPE', i, 4)
            f3 = f3 + ' - ' + ' - '.join(TYPE)
#        print(f3)

        constraints = constraints + [f1 + f2 + f3 + ' >= 0']

        return constraints
    
    def genModel_trunc(self, C, r):

        C = C + self.genConstraints_init(r)
        for i in range(0, r):
            C = C + self.genConstraints_of_Round(i)
        C = C + self.genConstraints_additional(r)

        V1 = getVariables_binary_Constraints(C)
        V2 = getVariables_integer_Constraints(C)

        filename='joltik' + str(self.keysize) + '_boom_' + str(r) + '.lp'
        o=open(filename,'w')

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

        o.write('Integer\n')
        for v in V2:
            o.write(v)
            o.write('\n')
        o.close()


if __name__ == '__main__':
    print('Initialized...')
    r = 5
    keysize = 128

    m = joltik_boom(keysize)

    constraints = []
    m.genModel_trunc(constraints, r)
    m=read("joltik" + str(keysize) + "_boom_" + str(r) + ".lp")
    m.optimize()
    # for v in m.getVars() :
    #     print(v.varName,v.x)

    m.write("joltik" + str(keysize) + "_boom_" + str(r) + ".sol")
