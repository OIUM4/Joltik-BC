import os
from joltik_boom_find import joltik_boom
from joltik_diff_find import joltik_diff
from gurobipy import *


if __name__ == '__main__':
    print('Initialized...')
    r = 4
    keysize = 128

    constraint = list([])
    file = [[], []]
    obj = 0
    g = ''
    while 1:
        m = joltik_boom(keysize)

        if g != '': constraints = [g + " >= " + str(obj)] + constraint
        else : constraints = constraint

        m.genModel_trunc(constraints, r)
        filename = "joltik" + str(keysize) + "_boom_" + str(r)
        with open(filename + ".lp", 'r', encoding='utf-8') as f:
            g = f.readline()
            g = f.readline()[:-1]

        o = read(filename + ".lp")
        #os.remove(filename + ".lp")
        o.Params.timelimit = 600
        o.Params.IntegralityFocus = 1
        o.optimize()
        obj = int(o.objVal)
        o.write(filename + ".sol")
        mb = 0
        with open(filename + ".sol", 'r', encoding='utf-8') as f:
            print(f.readline())
            for line in f.readlines():
                if line[:4] == "x_0_" and int(line[-2:-1]) == 1:
                    mb = mb +1
        m = joltik_diff(keysize)
        file = filename + ".sol"
        m.genModel(file, r)
        o = read("joltik" + str(keysize) + "_diff_" + str(r) + '.lp')
        os.remove("joltik" + str(keysize) + "_diff_" + str(r) + '.lp')
        o.optimize()

        print("mb:", mb)
        if o.status == 2 and int(o.objVal) + 4 * mb <= 29:


            path_trail = "joltik" + str(keysize) + "_diff_" + str(r) + ".sol"
            o.write(path_trail)

            P = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

            var = 'x'
            print("\n\n——————Differential trail——————")
            C = []
            with open(path_trail, 'r', encoding='utf-8') as f:
                print(f.readline())
                for line in f.readlines():
                    if line[:len(var)] == var and int(line[-2:-1]) == 1:
                        C.append(line[:-3])
            for i in range(r + 1):
                for j in range(16):
                    sum = 0
                    for k in range(3, -1, -1):
                        sum = 2 * sum
                        vars = var + '_' + str(i) + '_' + str(j) + '_' + str(k)
                        if vars in C:
                            sum = sum + 1
                    print(P[sum], end="")
                print()
            break
        else:
            var = 'x'
            C = []
            with open(filename + ".sol", 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    if line[:len(var)] == var and int(line[-2: -1]) == 1:
                        C.append(line[:-3])
            f = ''
            sum = 0
            for i in range(r):
                for j in range(16):
                    v = var + '_' + str(i) + '_' + str(j)
                    if v in C:
                        sum = sum + 1
                        f = f + " - " + v
                    else:
                        f = f + ' + ' + v
            constraint = [f + " >= " + str(1 - sum)] + constraint


