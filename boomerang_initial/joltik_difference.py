import os
from round_fountion_bit import *
from gurobipy import *

class joltik_diff():
    def __init__(self, keysize):
        assert keysize == 128 or keysize == 192
        self.s = int(keysize / 64)
        self.keysize = keysize


    def gen_Objective(self, r):
        assert r >= 0
        f = ''
        for i in range(r):
            y = genVars_InVars_at_Round('p', i, 2)
            for t in y:
                f = f + " + 3 " + t[0]
                f = f + " + 2 " + t[1]
        return f[3:]

    def genConstraints_state_Round(self, r):
        assert r >= 0
        constraints = list()

        X0 = genVars_InVars_at_Round('x', r, 4)
        Y = genVars_InVars_at_Round('y', r, 4)
        p = genVars_InVars_at_Round('p', r, 2)
        for i in range(len(Y)):
            constraints = constraints + SN(X0[i], Y[i], p[i])

        T = SR(Y)
        Z = genVars_InVars_at_Round('z', r, 4)
        MDS = genVars_InVars_at_Round('mds', r, 4)
        constraints = constraints + MN(T, Z, MDS)

        STK = genVars_InVars_at_Round('stk', r, 4)
        X1 = genVars_InVars_at_Round('x', r + 1, 4)
        constraints = constraints + xor(Z, STK, X1)

        return constraints

    def genConstraints_key_shedule(self, r):
        assert r >= 0

        constraints = list()
        TK = []
        for j in range(self.s):
            TK.append(genVars_InVars_at_Round(f"tk{j}", 0, 4))
        STK = genVars_InVars_at_Round('stk', 0, 4)
        constraints = constraints + key_xor(TK, STK)

        for i in range(1, r):
            TK0 = TK
            TK = []
            for j in range(self.s):
                TK.append(genVars_InVars_at_Round(f"tk{j}", i, 4))
            STK = genVars_InVars_at_Round('stk', i, 4)
            constraints = constraints + key_xor(TK, STK)
            TK0 = key_h(TK0)
            for j in range(16):
                for k in range(4):
                    constraints = constraints + [TK[0][j][k] + ' - ' + TK0[0][j][k] + ' = 0']
            for j in range(16):
                constraints = constraints + [TK[1][j][0] + ' - ' + TK0[1][j][3] + ' = 0']
                constraints = constraints + xor_bit(TK0[1][j][0], TK0[1][j][3], TK[1][j][1])
                constraints = constraints + [TK[1][j][2] + ' - ' + TK0[1][j][1] + ' = 0']
                constraints = constraints + [TK[1][j][3] + ' - ' + TK0[1][j][2] + ' = 0']
            if self.s == 3:
                for j in range(16):
                    constraints = constraints + [TK[2][j][0] + ' - ' + TK0[2][j][2] + ' = 0']
                    constraints = constraints + xor_bit(TK0[2][j][2], TK0[2][j][3], TK[2][j][1])
                    constraints = constraints + xor_bit(TK0[2][j][0], TK0[2][j][3], TK[2][j][2])
                    constraints = constraints + [TK[2][j][3] + ' - ' + TK0[2][j][1] + ' = 0']
        return constraints

    def genConstraints_addition(self, file, R):
        constraints = list()

        file_name = file[0]
        path = file[1]

        C = [[], []]
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                if line[3:4] == 'x':
                    if line[:2] == path:
                        if path == 'up' and getVariables_Round(line[3:]) <= R[0]:
                            C[int(line[-2:-1])].append(line[:-3][3:])
                        if path == "lo" and getVariables_Round(line[3:]) >= R[1]:
                            C[int(line[-2:-1])].append(changeVariables_Round(line[:-3][3:], R[1]))
                if line[3:6] == 'stk':
                    if line[:2] == path:
                        if path == 'up' and getVariables_Round(line[3:]) < R[0]:
                            C[int(line[-2:-1])].append(line[:-3][3:])
                        if path == "lo" and getVariables_Round(line[3:]) >= R[1]:
                            C[int(line[-2:-1])].append(changeVariables_Round(line[:-3][3:], R[1]))

        for x in C[0]:
            f = ''
            for i in range(4):
                f = f + ' + ' + x + '_' + str(i)
            f = f + ' = 0'
            constraints = constraints + [f[3:]]

        for x in C[1]:
            f = ''
            for i in range(4):
                f = f + ' + ' + x + '_' + str(i)
            f = f + ' >= 1'
            constraints = constraints + [f[3:]]

        return constraints


    def genModel(self, file, R):
        if file[1] == 'up':
            r = R[0]
        if file[1] == 'lo':
            r = R[2]

        C = list([])
        for i in range(0, r):
            C = C + self.genConstraints_state_Round(i)
        C = C + self.genConstraints_key_shedule(r)
        C = C + self.genConstraints_addition(file, R)

        V1 = getVariables_binary_Constraints(C)
        V2 = getVariables_General_Constraints(C)

        filename = 'joltik' + str(self.keysize) + '_diff_' + f'({R[0]}, {R[1]}, {R[2]})' + "_" + file[1] + '.lp'
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
        o.write('\n')

        o.write('Integer\n')
        for v in V2:
            o.write(v)
            o.write('\n')
        o.write('\n')
        o.close()


if __name__ == '__main__':
    print('Initialized...')

    keysize = 128
    r = [5, 2, 5]
    path = 'up'


    file = [f"joltik{keysize}_boom_({r[0]}, {r[1]}, {r[2]}).sol", path]

    m = joltik_diff(keysize)

    m.genModel(file, r)
    m = read('joltik' + str(keysize) + '_diff_' + f'({r[0]}, {r[1]}, {r[2]})' + "_" + path + '.lp')
    m.optimize()
    # for v in m.getVars():
    #     print(v.varName, v.x)

    m.write('joltik' + str(keysize) + '_diff_' + f'({r[0]}, {r[1]}, {r[2]})' + "_" + path + ".sol")
