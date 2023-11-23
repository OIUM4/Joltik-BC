import numpy as np
S=[14, 4, 11, 2, 3, 8, 0, 9, 1, 10, 7, 15, 6, 12, 5, 13]

def bin4(a):
    s=bin(a)[2:]
    while len(s)<4:
        s='0'+s
    x=[]
    for i in range(4):
        x.append(int(s[i]))
    return x

print("\t\t\t\t\t\t\tDDT")
DDT=np.zeros([16,16])
for i in range(16):
    for j in range(16):
        a=j
        b=i^j
        s=S[a]^S[b]
        DDT[i][s]=DDT[i][s]+1
print(DDT)

print("\t\t\t\t\t\t\tBCT")
BCT = np.zeros([16,16])
for n in range(16):
    for i in range(16):
        for j in range(16):
            a = S[n] ^ j
            b = S[n ^ i] ^ j
            if S.index(a) ^ S.index(b) == i:
                BCT[i][j] += 1
print(BCT)


# UBCT = np.zeros([16, 16, 16])
#
# for n in range(16):
#     for in_i in range(16):
#         for out_o in range(16):
#             a = S[n] ^ out_o
#             b = S[n ^ in_i] ^ out_o
#             if S.index(a) ^ S.index(b) == in_i:
#                 UBCT[in_i][S[n] ^ S[n ^ in_i]][out_o] += 1
# print(UBCT)
# print(UBCT[)


# H=[]
# NH=[]
# PH=[]
# for i in range(16):
#     for j in range(16):
#         if(DDT[i][j]!=0):
#             H.append(bin4(i)+bin4(j))
#             if(DDT[i][j]==16):
#                 p=[0,0]
#             if(DDT[i][j]==2):
#                 p=[1,0]
#             if (DDT[i][j]==4):
#                 p = [0, 1]
#             PH.append(bin4(i)+bin4(j)+p)
#         else:
#             NH.append(bin4(i) + bin4(j))
#
# print(H)
# print(PH)

