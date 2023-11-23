if __name__ == "__main__":
    # r = [4, 1, 3]
    # keysize = 128
    # #path = 'trail/joltik-128/4, 1, 4/'
    # file = [f"joltik{keysize}_diff_({r[0]}, {r[1]}, {r[2]})_up.sol", f"joltik{keysize}_diff_({r[0]}, {r[1]}, {r[2]})_lo.sol"]
    #
    # P = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    #
    # var = 'tk1'    #x    y    stk    z    tk0    tk1    tk2
    # print("————————————————————upper trail————————————————————")
    # C = []
    # with open(file[0], 'r', encoding='utf-8') as f:
    #     for line in f.readlines()[1:]:
    #         if line[:len(var)] == var and int(line[-2:-1]) == 1:
    #             C.append(line[:-3])
    # for i in range(r[0] + 1):
    #     for j in range(16):
    #         sum = 0
    #         for k in range(3, -1, -1):
    #             sum = 2 * sum
    #             vars = var + '_' + str(i) + '_' + str(j) + '_' + str(k)
    #             if vars in C:
    #                 sum = sum + 1
    #         print(P[sum], end="")
    #     print()
    #
    # print("\n\n——————lower trail——————")
    # C = []
    # with open(file[1], 'r', encoding='utf-8') as f:
    #     for line in f.readlines()[1:]:
    #         if line[:len(var)] == var and int(line[-2:-1]) == 1:
    #             C.append(line[:-3])
    # for i in range(r[2] + 1):
    #     for j in range(16):
    #         sum = 0
    #         for k in range(3, -1, -1):
    #             sum = 2 * sum
    #             vars = var + '_' + str(i) + '_' + str(j) + '_' + str(k)
    #             if vars in C:
    #                 sum = sum + 1
    #         print(P[sum], end="")
    #     print()




    C = []
    var = 'tk1'
    with open("joltik128_diff_(1, 3, 1)_lo.sol", 'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            if line[:len(var)] == var and int(line[-2:-1]) == 1:
                C.append(line[:-3])
    print(C)
    for i in range(0, 6):
        for j in range(16):
            sum = 0
            for k in range(3, -1, -1):
                sum = 2 * sum
                vars = var + '_' + str(i) + '_' + str(j) + '_' + str(k)
                if vars in C:
                    sum = sum + 1
            print(hex(sum)[2:], end="")
        print()