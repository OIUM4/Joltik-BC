def genVars_InVars_at_Round(STR, r, n):
    assert r >= 0
    return [STR + '_' + str(r) + '_' + str(j) for j in range(n)]

def SR(X):
    n = len(X)
    temp = [None] * n
    T = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    for i in range(n):
        temp[i] = X[T[i]]
    return temp

def h(X):
    n = len(X)
    temp = [None] * n
    T = [7, 0, 13, 10, 11, 4, 1, 14, 15, 8, 5, 2, 3, 12, 9, 6]
    for i in range(n):
        temp[i] = X[T[i]]
    return temp

def ART(x, y, z):
    constraints = []
    for i in range(len(x)):
        constraints += [x[i] + ' + ' + y[i] + ' - ' + z[i] + ' >= 0']
        constraints += [x[i] + ' - ' + y[i] + ' + ' + z[i] + ' >= 0']
        constraints += ['- ' + x[i] + ' + ' + y[i] + ' + ' + z[i] + ' >= 0']
    return constraints

def ART_inner(x, y, z):
    constraints = []
    for i in range(len(x)):
        constraints += [z[i] + ' - ' + x[i] + ' >= 0']
        constraints += [z[i] + ' - ' + y[i] + ' >= 0']
        constraints += [x[i] + ' + ' + y[i] + ' - ' + z[i] + ' >= 0']
    return constraints

def ART_c(x, y, z, c):
    constraints = []
    for i in range(len(x)):
        constraints += ['- ' + x[i] + ' - ' + y[i] + ' + ' + z[i] + ' + ' + c[i] + ' >= -1']
        constraints += [x[i] + ' + ' + y[i] + ' + ' + z[i] + ' - ' + c[i] + ' >= 0']
        constraints += [x[i] + ' - ' + y[i] + ' - ' + z[i] + ' - ' + c[i] + ' >= -2']
        constraints += ['- ' + x[i] + ' + ' + y[i] + ' - ' + z[i] + ' - ' + c[i] + ' >= -2']
        constraints += ['- ' + x[i] + ' - ' + y[i] + ' - ' + z[i] + ' - ' + c[i] + ' >= -3']
    return constraints


def MN(x, y, d):
    constraints = []
    n = int(len(x) / 4)
    for i in range(n):
        constraints += [x[4 * i + 0] + ' + ' + x[4 * i + 1] + ' + ' + x[4 * i + 2] + ' + ' + x[4 * i + 3] + ' + ' + y[
            4 * i + 0] + ' + ' + y[4 * i + 1] + ' + ' + y[4 * i + 2] + ' + ' + y[4 * i + 3] + ' - 5 ' + d[i] + ' >= 0']
        constraints += [x[4 * i + 0] + ' + ' + x[4 * i + 1] + ' + ' + x[4 * i + 2] + ' + ' + x[4 * i + 3] + ' + ' + y[
            4 * i + 0] + ' + ' + y[4 * i + 1] + ' + ' + y[4 * i + 2] + ' + ' + y[4 * i + 3] + ' - 8 ' + d[i] + ' <= 0']
    return  constraints

def MN_out(x, y):
    constraints = []
    n = int(len(x) / 4)
    for i in range(n):
        for j in range(4):
            constraints += ['4 ' + y[4 * i + j] + ' - ' + x[4 * i + 0] + ' - ' + x[4 * i + 1] + ' - ' + x[4 * i + 2] + ' - ' + x[4 * i + 3] + ' >= 0']
            constraints += [x[4 * i + 0] + ' + ' + x[4 * i + 1] + ' + ' + x[4 * i + 2] + ' + ' + x[4 * i + 3] + ' - ' + y[4 * i + j] + ' >= 0']
    return constraints




def key_shedule(x, y, r, s):
    constraints = []
    for i in range(16):
        f = []
        for j in range(r):
            f.append(y[j][i])
        f = ' + '.join(f)
        constraints += [f + ' - ' + str(r) + ' ' + x[i] + ' >= - ' + str(s - 1)]
        constraints += [f + ' - ' + str(r) + ' ' + x[i] + ' <= 0']
    return constraints

def middle_constraints(x, y, z):
    constraints = []
    for i in range(16):
        constraints += [x[i] + ' - ' + z[i] + ' >= 0']
        constraints += [y[i] + ' - ' + z[i] + ' >= 0']
        constraints += ['- ' + x[i] + ' - ' + y[i] + ' + ' + z[i] + ' >= -1']
    return constraints


def getVariables_binary(r1, rm, r2):
    V = [f'up_LANE_{i}' for i in range(16)]
    for i in range(r1 + rm):
        V = V + genVars_InVars_at_Round('up_x', i, 16)
        V = V + genVars_InVars_at_Round('up_stk', i, 16)
        V = V + genVars_InVars_at_Round('up_y', i, 16)
        V = V + genVars_InVars_at_Round('up_d', i, 4)
        if i < r1:
            V = V + genVars_InVars_at_Round('up_c', i + 1, 16)
    V = V + genVars_InVars_at_Round('up_x', r1 + rm, 16)
    V = V + genVars_InVars_at_Round('up_stk', r1 + rm, 16)
    V = V + genVars_InVars_at_Round('up_y', r1 + rm, 16)

    V = V + [f'lo_LANE_{i}' for i in range(16)]
    for i in range(rm + r2):
        V = V + genVars_InVars_at_Round('lo_x', i, 16)
        V = V + genVars_InVars_at_Round('lo_stk', i, 16)
        V = V + genVars_InVars_at_Round('lo_y', i, 16)
        V = V + genVars_InVars_at_Round('lo_d', i, 4)
        if i >= rm:
            V = V + genVars_InVars_at_Round('lo_c', i + 1, 16)
    V = V + genVars_InVars_at_Round('lo_x', rm + r2, 16)
    V = V + genVars_InVars_at_Round('lo_stk', rm + r2, 16)
    V = V + genVars_InVars_at_Round('lo_y', rm + r2, 16)

    for i in range(rm):
        V = V + genVars_InVars_at_Round('mi_y', i, 16)

    # V = set([])
    # for s in C:
    #     temp = s.strip()
    #     temp = temp.replace('+', ' ')
    #     temp = temp.replace('-', ' ')
    #     temp = temp.replace('>=', ' ')
    #     temp = temp.replace('<=', ' ')
    #     temp = temp.split()
    #     for v in temp:
    #         if not v.isdigit() and v[3:7] != 'TYPE':
    #             V.add(v)
    return V

def getVariables_integer(r1, rm, r2):
    V = []
    for i in range(r1 + rm):
        V = V + genVars_InVars_at_Round('up_TYPE', i, 4)
    for i in range(rm + r2):
        V = V + genVars_InVars_at_Round('lo_TYPE', i, 4)

    # for s in C:
    #     temp = s.strip()
    #     temp = temp.replace('+', ' ')
    #     temp = temp.replace('-', ' ')
    #     temp = temp.replace('>=', ' ')
    #     temp = temp.replace('<=', ' ')
    #     temp = temp.split()
    #     for v in temp:
    #         if v[3:7] == 'TYPE':
    #             V.add(v)
    return V

def getVariables_binary_Constraints(C):
    V = set([])
    for s in C:
        temp = s.strip()
        temp = temp.replace('+', ' ')
        temp = temp.replace('-', ' ')
        temp = temp.replace('>=', ' ')
        temp = temp.replace('<=', ' ')
        temp = temp.split()
        for v in temp:
            if not v.isdigit() and v[3:7] != 'TYPE':
                V.add(v)
    return V

def getVariables_integer_Constraints(C):
    V = set([])
    for s in C:
        temp = s.strip()
        temp = temp.replace('+', ' ')
        temp = temp.replace('-', ' ')
        temp = temp.replace('>=', ' ')
        temp = temp.replace('<=', ' ')
        temp = temp.split()
        for v in temp:
            if v[3:7] == 'TYPE':
                V.add(v)
    return V

if __name__ == "__main__":
    print(len(getVariables_binary(5, 1, 5)))