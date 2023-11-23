def B1(a,i):
    answers = [ele for ele in a]
    answers[i] = (answers[i] + 1) % 2
    return answers

def list_union(a,b):
    answers=[ele for ele in a]
    for ele in b:
        if ele not in a:
            answers.append(ele)
    return answers

def list_difference(a,b):
    answers=[ele for ele in a]
    for ele in b:
        if ele in a:
            answers.remove(ele)
    return answers

def list_intersection(a,b):
    answers=[]
    for ele in b:
        if ele in a:
            answers.append(ele)
    return answers

def prec_form(apoints,n):
    OUT = []
    for a in apoints:
        s = []
        S = []
        U = []
        for i in range(n + 1):
            S.append([])
            U.append([])

        for b in apoints:
            u = [(int(a[i]) + int(b[i])) % 2 for i in range(n)]
            sum = 0
            w = 0
            for i in range(n):
                sum = sum + int(a[i]) * int(u[i])
                w = w + int(u[i])
            if sum == 0:
                if u not in U[w]: U[w].append(u)

        if len(U[1]) == 0:
            for x in U[0]:
                OUT.append([a, x])
            continue
        else:
            for x in U[1]:
                s.append([a, x])

        for x in U[0]:
            S[0].append([a, x])
        for x in U[1]:
            S[1].append([a, x])

        k = 2
        while k <= n:
            if len(U[k]) == 0:
                k = k + 1
                break
            for u in U[k]:
                o = 1
                for i in range(n):
                    v = u.copy()
                    if u[i] == 1:
                        v[i] = 0
                        if [a, v] not in S[k - 1]:
                            o = 0
                            break
                if o == 1:
                    S[k].append([a, u])
                    for i in range(n):
                        v = u.copy()
                        if u[i] == 1:
                            v[i] = 0
                            if [a, v] in s: s.remove([a, v])
            for x in S[k]:
                s.append(x)
            k = k + 1
        for x in s:
            OUT.append(x)
    inequality = []
    for x in OUT:
        sum = 0
        c = []
        for i, j in zip(x[0], x[1]):
            sum = sum + int(i)
            if int(i) == 1:
                c.append(-1)
            else:
                if int(j) == 0:
                    c.append(1)
                else:
                    c.append(0)
        c.append(sum - 1)
        inequality.append(c)
    return inequality

def three_balls_form(apoints,n):
    C = []
    near = []
    for a in apoints:
        near_a = []
        for b in apoints:
            if a != b:
                sum = 0
                for i in range(n):
                    sum = sum + (a[i] + b[i]) % 2
                if sum == 1: near_a.append(b)
        near.append(near_a)
    for a, x in zip(apoints, near):
        if len(x) >= 2:
            i = 0
            while i < len(x):
                j = i + 1
                m = 0
                while j < len(x):
                    if m == 0:
                        b = x[i]
                        c = x[j]
                    else:
                        b = x[j]
                        c = x[i]
                    d = [(a[k] + b[k] + c[k]) % 2 for k in range(n)]
                    if d in apoints:
                        Ba = list_union([B1(a, k) for k in range(n)], [a])
                        Bb = list_union([B1(b, k) for k in range(n)], [b])
                        Bc = list_union([B1(c, k) for k in range(n)], [c])
                        Pa = list_difference(Ba, apoints)
                        Ra = list_union(Pa, [c])
                        Pb = list_difference(Bb, apoints)
                        Rb = [k for k in Pb]
                        Rc = list_difference(Bc, apoints)
                        for p in Pa:
                            e = [(p[k] + a[k] + b[k]) % 2 for k in range(n)]
                            Rb = list_union(Rb, [e])
                            e = [(p[k] + a[k] + c[k]) % 2 for k in range(n)]
                            Rc = list_union(Rc, [e])
                        for p in Pb:
                            e = [(p[k] + b[k] + c[k]) % 2 for k in range(n)]
                            Rc = list_union(Rc, [e])
                        Q = list_union(list_union(Pa, Rb), Rc)
                        na = [0] * (n + 1)
                        nb = [0] * (n + 1)
                        nc = [0] * (n + 1)
                        for k in range(n):
                            if (c[k] + a[k]) % 2 == 1:
                                t = 2
                            else:
                                t = 1
                                for q in list_intersection(Q, Ba):
                                    if (q[k] + a[k]) % 2 == 1:
                                        t = 2
                                        break
                            na[k] = na[k] + t * (1 - 2 * a[k])
                            na[n] = na[n] + t * a[k]
                            t = 1
                            for q in list_intersection(Q, Bb):
                                if (q[k] + b[k]) % 2 == 1:
                                    t = 2
                                    break
                            nb[k] = nb[k] + t * (1 - 2 * b[k])
                            nb[n] = nb[n] + t * b[k]
                            t = 1
                            for q in list_intersection(Q, Bc):
                                if (q[k] + c[k]) % 2 == 1:
                                    t = 2
                                    break
                            nc[k] = nc[k] + t * (1 - 2 * c[k])
                            nc[n] = nc[n] + t * c[k]
                        new = [na[k] + nb[k] + nc[k] for k in range(n + 1)]
                        new[n] = new[n] - 8
                        C = list_union(C, [new])
                    if m == 1: j = j + 1
                    m = (m + 1) % 2
                i = i + 1
    return C

def one_balls_form(apoints,n):
    C=[]
    for a in apoints:
        B = list_union([B1(a, k) for k in range(n)], [a])
        Q = list_difference(B, apoints)
        new = [0] * (n + 1)
        for k in range(n):
            t = 1
            for q in Q:
                if (q[k] + a[k]) % 2 == 1:
                    t = 2
                    break
            new[k] = new[k] + t * (1 - 2 * a[k])
            new[n] = new[n] + t * a[k]
        new[n] = new[n] - 2
        C.append(new)
    return C