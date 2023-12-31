from gurobipy import *
from inequality_generate import *


if __name__ == "__main__":
    points = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
              [0, 0, 0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
              [0, 0, 1, 0, 0, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
              [0, 0, 1, 1, 1, 0, 0, 0, 1, 0], [0, 0, 1, 1, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
              [0, 0, 1, 1, 1, 0, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0, 1, 0], [0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 1, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
              [0, 1, 0, 0, 0, 1, 1, 0, 1, 0], [0, 1, 0, 0, 0, 1, 1, 1, 1, 0], [0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
              [0, 1, 0, 0, 1, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 1, 0, 1, 1, 0], [0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
              [0, 1, 0, 1, 0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
              [0, 1, 0, 1, 1, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 1, 0, 1, 1, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
              [0, 1, 1, 0, 0, 0, 1, 1, 1, 0], [0, 1, 1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
              [0, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
              [0, 1, 1, 0, 1, 1, 1, 0, 1, 0], [0, 1, 1, 1, 0, 0, 0, 1, 1, 0], [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
              [0, 1, 1, 1, 1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
              [1, 0, 0, 0, 1, 1, 0, 1, 1, 0], [1, 0, 0, 0, 1, 1, 1, 0, 1, 0], [1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
              [1, 0, 0, 1, 0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
              [1, 0, 0, 1, 1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 1, 1, 1, 0, 1, 0], [1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
              [1, 0, 1, 0, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 0, 1, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
              [1, 0, 1, 0, 1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
              [1, 0, 1, 1, 0, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 1, 1, 0, 0, 1, 0],
              [1, 0, 1, 1, 1, 1, 0, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0, 1, 0], [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 0, 0, 1, 0, 0, 1], [1, 1, 0, 0, 0, 1, 1, 0, 1, 0], [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 1, 0, 0, 0, 0, 1], [1, 1, 0, 0, 1, 1, 1, 0, 1, 0], [1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
              [1, 1, 0, 1, 0, 0, 1, 0, 0, 1], [1, 1, 0, 1, 0, 1, 1, 0, 1, 0], [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
              [1, 1, 0, 1, 1, 0, 0, 1, 0, 1], [1, 1, 0, 1, 1, 1, 1, 0, 1, 0], [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
              [1, 1, 1, 0, 0, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0, 1, 1, 1, 0], [1, 1, 1, 0, 0, 1, 0, 0, 1, 0],
              [1, 1, 1, 0, 0, 1, 1, 1, 1, 0], [1, 1, 1, 0, 1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
              [1, 1, 1, 0, 1, 1, 0, 1, 1, 0], [1, 1, 1, 0, 1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
              [1, 1, 1, 1, 0, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
              [1, 1, 1, 1, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 0, 1, 0, 1, 0], [1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
    n = len(points[0])
    apoints = []
    for i in range(2 ** n):
        a = []
        for j in bin(i)[2:]:
            a.append(int(j))
        while (len(a) < n):
            a = [0] + a
        if a not in points:
            apoints.append(a)

    inequalitys = []
    with open('sbox_init.txt', ) as f:
        for line in f.readlines():
            temp = line.split()
            for i in range(len(temp)):
                temp[i] = int(temp[i])
            inequalitys.append(temp)
    inequalitys = list_union(prec_form(apoints, n), inequalitys)
    inequalitys = list_union(three_balls_form(apoints, n), inequalitys)
    inequalitys = list_union(one_balls_form(apoints, n), inequalitys)
    add = []
    for x in apoints:
        c = []
        for i in range(len(inequalitys)):
            sum = 0
            for j in range(n):
                sum = sum + x[j] * inequalitys[i][j]
            sum = sum + inequalitys[i][n]
            if sum < 0: c.append(i)
        add.append(c)
    z = []
    a = len(inequalitys)
    for x in range(a):
        z.append('z%d' % x)

    try:

        # Create a new model
        model = Model("mip1")

        # Create variables
        for i in range(a):
            z[i] = model.addVar(vtype=GRB.BINARY, name='z%d' % i)

        # Set objective
        sum = 0
        for x in z:
            sum = sum + x
        model.setObjective(sum, GRB.MINIMIZE)

        # Add constraint:
        for x in add:
            sum = 0
            for y in x:
                sum = sum + z[y]
            model.addConstr(sum >= 1, "c")
        del (add)

        model.optimize()

        with open('sbox_inequality.txt', 'w') as h:
            for v in model.getVars():
                if v.x == 1.0:
                    a = int(v.varName[1:])
                    for x in inequalitys[a]:
                        h.write(str(x) + ' ')
                    h.write('\n')

        print('Obj:', model.objVal)

    except GurobiError:
        print('Error reported')




