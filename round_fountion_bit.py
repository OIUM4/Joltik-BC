def genVars_InVars_at_Round(STR ,r, n):
    assert r >= 0
    return [[STR + '_' + str(r) + '_' + str(j) + '_' + str(i) for i in range(n)] for j in range(16)]

def xor(x, y, z):
    constraints = []
    for i in range(len(x)):
        for j in range(len(x[i])):
            constraints += [x[i][j] + ' + ' + y[i][j] + ' + ' + z[i][j] + ' <= 2']
            constraints += [x[i][j] + ' + ' + y[i][j] + ' - ' + z[i][j] + ' >= 0']
            constraints += [x[i][j] + ' - ' + y[i][j] + ' + ' + z[i][j] + ' >= 0']
            constraints += ['- ' + x[i][j] + ' + ' + y[i][j] + ' + ' + z[i][j] + ' >= 0']
    return constraints

def xor_bit(x, y, z):
    constraints = [x + ' + ' + y + ' + ' + z + ' <= 2']
    constraints += [x + ' + ' + y + ' - ' + z + ' >= 0']
    constraints += [x + ' - ' + y + ' + ' + z + ' >= 0']
    constraints += ['- ' + x + ' + ' + y + ' + ' + z + ' >= 0']
    return constraints

def SN(x, y, p):
    constraints = []
    sbox = x[::-1] + y[::-1] + p

    inequality = []
    with open('sbox_inequality.txt', ) as f:
        for line in f.readlines():
            temp = line.split()
            inequality.append(temp)

    for i in range(len(inequality)):
        s = ''
        if int(inequality[i][0]) != 0:
            s = inequality[i][0] + ' ' + sbox[0]
        for j in range(1, len(sbox)):
            if int(inequality[i][j]) > 0:
                s = s + ' + ' + inequality[i][j] + ' ' + sbox[j]
            if int(inequality[i][j]) < 0:
                s = s + ' - ' + inequality[i][j][1:] + ' ' + sbox[j]
        s = s + ' >= ' + str(-int(inequality[i][j + 1]))
        constraints += [s]
    return constraints

def SR(X):
    n = len(X)
    temp = [None] * n
    T = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    for i in range(n):
        temp[i] = X[T[i]]
    return temp

def MN(X, Y, MDS):
    constraints = []
    M = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
         [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
         [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
         [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
         [0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
         [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
         [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]]

    for t in range(4):
        x = X[4 * t + 0][::-1] + X[4 * t + 1][::-1] + X[4 * t + 2][::-1] + X[4 * t + 3][::-1]
        y = Y[4 * t + 0][::-1] + Y[4 * t + 1][::-1] + Y[4 * t + 2][::-1] + Y[4 * t + 3][::-1]
        mds = MDS[4 * t + 0][::-1] + MDS[4 * t + 1][::-1] + MDS[4 * t + 2][::-1] + MDS[4 * t + 3][::-1]
        for i in range(len(M)):
            s = ""
            sum = 1
            for j in range(len(M[i])):
                if M[i][j] == 1:
                    sum = sum + 1
                    s = s + " + " + x[j]
            s = s + " + " + y[i] + " - 2 " + mds[i] + " =  0"
            constraints = constraints + [s[3:]]
            constraints = constraints + [mds[i] + " <= " + str(int(sum/2))]
            constraints = constraints + [mds[i] + " >= 0"]
    return constraints

def key_xor(TK, STK):
    constraints = []

    if len(TK) == 2:
        for i in range(16):
            for j in range(4):
                constraints = constraints + [TK[0][i][j] + ' + ' + TK[1][i][j] + ' + ' + STK[i][j] + ' <= 2']
                constraints = constraints + [TK[0][i][j] + ' + ' + TK[1][i][j] + ' - ' + STK[i][j] + ' >= 0']
                constraints = constraints + [TK[0][i][j] + ' - ' + TK[1][i][j] + ' + ' + STK[i][j] + ' >= 0']
                constraints = constraints + [' - ' + TK[0][i][j] + ' + ' + TK[1][i][j] + ' + ' + STK[i][j] + ' >= 0']
    if len(TK) == 3:
        for i in range(16):
            for j in range(4):
                constraints = constraints + [TK[0][i][j] + ' + ' + TK[1][i][j] + ' + ' + TK[2][i][j] + ' - ' + STK[i][j] + ' >= 0']
                constraints = constraints + [TK[0][i][j] + ' + ' + TK[1][i][j] + ' - ' + TK[2][i][j] + ' + ' + STK[i][j] + ' >= 0']
                constraints = constraints + [TK[0][i][j] + ' - ' + TK[1][i][j] + ' + ' + TK[2][i][j] + ' + ' + STK[i][j] + ' >= 0']
                constraints = constraints + [TK[0][i][j] + ' - ' + TK[1][i][j] + ' - ' + TK[2][i][j] + ' - ' + STK[i][j] + ' >= -2']
                constraints = constraints + [' - ' + TK[0][i][j] + ' + ' + TK[1][i][j] + ' + ' + TK[2][i][j] + ' + ' + STK[i][j] + ' >= 0']
                constraints = constraints + [' - ' + TK[0][i][j] + ' + ' + TK[1][i][j] + ' - ' + TK[2][i][j] + ' - ' + STK[i][j] + ' >= -2']
                constraints = constraints + [' - ' + TK[0][i][j] + ' - ' + TK[1][i][j] + ' + ' + TK[2][i][j] + ' - ' + STK[i][j] + ' >= -2']
                constraints = constraints + [' - ' + TK[0][i][j] + ' - ' + TK[1][i][j] + ' - ' + TK[2][i][j] + ' + ' + STK[i][j] + ' >= -2']

    return constraints

def key_h(TK):
    T = [1, 6, 11, 12, 5, 10, 15, 0, 9, 14, 3, 4, 13, 2, 7, 8]
    for x in range(len(TK)):
        n = len(TK[x])
        temp = [None] * n
        for i in range(n):
            temp[i] = TK[x][T[i]]
        TK[x] = temp
    return TK

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
            if not v.isdigit() and v[:3] != 'mds':
                V.add(v)
    return V

def getVariables_General_Constraints(C):
    V = set([])
    for s in C:
        temp = s.strip()
        temp = temp.replace('+', ' ')
        temp = temp.replace('-', ' ')
        temp = temp.replace('>=', ' ')
        temp = temp.replace('<=', ' ')
        temp = temp.split()
        for v in temp:
            if v[:3] == 'mds':
                V.add(v)
    return V


def getVariables_Round(s):
    r = ''
    for i in range(len(s)):
        if s[i] == '_':
            j = i + 1
            while s[j] != '_':
                r = r + s[j]
                j += 1
            break
    return int(r)

def changeVariables_Round(s, rm):
    r = str(getVariables_Round(s) - rm)
    for i in range(len(s)):
        if s[i] == '_':
            j = i + 1
            s0 = s[:j]
            while s[j] != '_': j += 1
            s1 = s[j:]
            break
    s = s0 + r + s1
    return s


def truncated_bits(X, x):
    constraints = []
    for i in range(len(X)):
        constraints = constraints + [' + '.join(x[i]) + ' - ' + X[i] + ' >= 0']
        for t in x[i]:
            constraints = constraints + [X[i] + ' - ' + t + ' >= 0']
    return constraints


if __name__ == "__main__":
    x = genVars_InVars_at_Round('x', 0, 4)

    X = [f"x_0_{j}" for j in range(16)]
    print(X,x)
    constraints = truncated_bits(X, x)
    for x in constraints:
        print(x)