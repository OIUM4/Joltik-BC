def add_poly(L1,L2):
    R=[]
    if len(L1)>len(L2):
        L1,L2=L2,L1
    i=0
    while i<len(L1):
        R.append(L1[i]+L2[i])
        i+=1
    R=R+L2[len(L1):len(L2)]
    for i in range(len(R)): R[i] = R[i] % 2
    while R[-1] == 0 and len(R) > 1: R = R[:-1]
    return R


def multiply_poly(L1,L2):#多项式乘法
    if len(L1)>len(L2):
        L1,L2=L2,L1
    zero=[];R=[]
    for i in L1:
        T=zero[:]
        for j in L2:
            T.append(i*j)
        R=add_poly(R,T)
        zero=zero+[0]
    for i in range(len(R)): R[i] = R[i] % 2
    while R[-1] == 0 and len(R) > 1 : R = R[:-1]
    return R

def bin_list(x):
    R=[]
    if x == 0: R=[0]
    while x != 0:
        R = R + [x % 2]
        x = int((x - x % 2) / 2)
    return R

def dec_list(x):
    sum = 0
    while  len(x) > 0:
        sum = sum * 2
        sum = sum + x[-1]
        x = x[:-1]
    return sum

def mod(x, y):
    while len(x) >= len(y):
        t = y
        while len(x) > len(t): t = [0] + t
        x = add_poly(x, t)
    return x

def field_multiply(M, X, field):
    n = len(X)
    Y = list()
    for i in range(n):
        sum = [0]
        for j in range(n):
            x = bin_list(M[i][j])
            y = bin_list(X[j])
            t = mod(multiply_poly(x, y), field)
            sum = add_poly(sum, t)
        Y.append(dec_list(sum))
    return Y


if __name__ == "__main__":
    field = [1, 1, 0, 0, 1]
    M = [[1, 4, 9, 13],
         [4, 1, 13, 9],
         [9, 13, 1, 4],
         [13, 9, 4, 1]]
    X = [11, 12, 5, 2]

    print(mod(multiply_poly([0, 1], [1, 0, 0, 1]), field))
    print(mod(multiply_poly([0, 0, 1], [1, 0, 1, 1]), field))


    print(field_multiply(M, X, field))
