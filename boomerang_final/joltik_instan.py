import os
from joltik_boom import joltik_boom
from joltik_diff import joltik_diff
from gurobipy import *


if __name__ == '__main__':
    print('Initialized...')
    r = [1, 4, 1, 3, 1]
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
        filename = "joltik" + str(keysize) + "_boom_" + f'({r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]})'
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

        path = ['up', 'lo']
        count = 0
        path_trail = [None] * 2
        for i in range(2):
            if r[2 * i] == 0:
                start = 0
            else:
                start = r[2 * i] - 1

            m = joltik_diff(keysize)
            file = [filename + ".sol", path[i]]
            m.genModel(file, r)
            o = read("joltik" + str(keysize) + "_diff_" + f'({r[2 * i]}, {r[2 * i + 1]}, {r[2 * i + 2]})' + "_" + path[i] + '.lp')
            #os.remove("joltik" + str(keysize) + "_diff_" + f'({r[2 * i]}, {r[2 * i + 1]}, {r[2 * i + 2]})' + "_" + path[i] + ".lp")
            o.optimize()

            if o.status == 2:
                count = count + 1
                path_trail[i] = "joltik" + str(keysize) + "_diff_" + f'({r[2 * i]}, {r[2 * i + 1]}, {r[2 * i + 2]})' + "_" + path[i] + ".sol"
                o.write(path_trail[i])
            else:
                var = 'x'
                C = []
                with open(filename + ".sol", 'r', encoding='utf-8') as f:
                    for line in f.readlines()[1:]:
                        if line[3: 4] == var and int(line[-2: -1]) == 1:
                            C.append(line[:-3])
                f = ''
                sum = 0
                for j in range(start, r[2 * i] + r[2 * i +1]):
                    for k in range(16):
                        v = path[i] + '_' + var + '_' + str(j) + '_' + str(k)
                        if v in C:
                            sum = sum + 1
                            f = f + " - " + v
                        else:
                            f = f + ' + ' + v
                constraint = [f + " >= " + str(1 - sum)] + constraint

                break

        if count == 2:
            P = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

            if r[0] == 0:
                start_up = 0
            else:
                start_up = r[0] - 1
            var = 'x'
            print("\n\n——————upper trail——————")
            C = []
            with open(path_trail[0], 'r', encoding='utf-8') as f:
                print(f.readline())
                for line in f.readlines():
                    if line[:len(var)] == var and int(line[-2:-1]) == 1:
                        C.append(line[:-3])
            for i in range(start_up, r[0] + r[1] + 1):
                for j in range(16):
                    sum = 0
                    for k in range(3, -1, -1):
                        sum = 2 * sum
                        vars = var + '_' + str(i) + '_' + str(j) + '_' + str(k)
                        if vars in C:
                            sum = sum + 1
                    print(P[sum], end="")
                print()

            if r[2] == 0:
                start_lo = 0
            else:
                start_lo = r[2] - 1
            print("\n\n——————lower trail——————")
            C = []
            with open(path_trail[1], 'r', encoding='utf-8') as f:
                print(f.readline())
                for line in f.readlines():
                    if line[:len(var)] == var and int(line[-2:-1]) == 1:
                        C.append(line[:-3])
            for i in range(start_lo, r[2] + r[3] + 1):
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
