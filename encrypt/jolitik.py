from numpy import *
from MDS import *
import random

class joltik():
    S_BOX = [0xe, 0x4, 0xb, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xa, 0x7, 0xf, 0x6, 0xc, 0x5, 0xd]
    Inv_S_BOX = [0x6, 0x8, 0x3, 0x4, 0x1, 0xe, 0xc, 0xa, 0x5, 0x7, 0x9, 0x2, 0xd, 0xf, 0x0, 0xb]
    MIX_C = [[0x1, 0x4, 0x9, 0xd], [0x4, 0x1, 0xd, 0x9], [0x9, 0xd, 0x1, 0x4], [0xd, 0x9, 0x4, 0x1]]
    Rc = [0x01, 0x03, 0x07, 0x0f, 0x1f, 0x3e, 0x3d, 0x3b, 0x37, 0x2f, 0x1e, 0x3c, 0x39, 0x33, 0x27, 0x0e, 0x1d, 0x3a,
          0x35, 0x2b, 0x16, 0x2c, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0b, 0x17, 0x2e, 0x1c, 0x38, 0x31]
    FIELD = [1, 1, 0, 0, 1]     # the irreducible polynomia 1 + x + x ^ 4

    def __init__(self, keysize):
        assert keysize == 128 or keysize == 192
        if keysize == 128:
            self.s = 2
            self.round = 24
        if keysize == 192:
            self.s = 3
            self.round = 32

    def SubNibbles(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        temp = ''
        for i in range(16):
            temp = temp + hex(self.S_BOX[int(s[i], 16)])[2:]

        return int(temp, 16)

    def Inv_SubNibbles(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        temp = ''
        for i in range(16):
            temp = temp + hex(self.Inv_S_BOX[int(s[i], 16)])[2:]

        return int(temp, 16)

    def ShiftRows(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        T = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
        temp = ''
        for i in range(16):
            temp = temp + s[T[i]]

        return int(temp, 16)

    def Inv_ShiftRows(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        T = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]
        temp = ''
        for i in range(16):
            temp = temp + s[T[i]]

        return int(temp, 16)

    def MixNibbles(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        temp = ''
        for i in range(4):
            a = []
            for j in range(4):
                a.append(int(s[4 * i + j], 16))
            a = field_multiply(self.MIX_C, a, self.FIELD)
            for j in range(4):
                temp = temp + hex(a[j])[2:]

        return int(temp, 16)

    def RCON(self, r):
        s = bin(self.Rc[r])[2:]
        while len(s) < 6:
            s = '0' + s

        sum = str(int(s[0] + s[1] + s[2], 2))
        sum = sum + str(int(s[3] + s[4] + s[5], 2))
        sum = sum + str(int(s[0] + s[1] + s[2], 2))
        sum = sum + str(int(s[3] + s[4] + s[5], 2))
        sum = '0123' + sum + '00000000'

        return int(sum, 16)

    def h(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        T = [1, 6, 11, 12, 5, 10, 15, 0, 9, 14, 3, 4, 13, 2, 7, 8]
        temp = ''
        for i in range(16):
            temp = temp + s[T[i]]

        return int(temp, 16)

    def Inv_h(self, x):
        s = hex(x)[2:]
        while len(s) < 16:
            s = '0' + s

        T = [7, 0, 13, 10, 11, 4, 1, 14, 15, 8, 5, 2, 3, 12, 9, 6]
        temp = ''
        for i in range(16):
            temp = temp + s[T[i]]

        return int(temp, 16)

    def TweakeySchedule(self, KT):
        s = hex(KT)[2:]
        while len(s) < self.s * 16:
            s = '0' + s

        TK = []
        for i in range(self.s):
            TK.append(int(s[i * 16:(i + 1) * 16], 16))

        # for x in TK:
        #    print(hex(x))

        STK = []
        temp = self.RCON(0)
        for x in TK:
            temp = x ^ temp
        STK.append(temp)

        for i in range(1, self.round + 1):
            for j in range(self.s):
                TK[j] = self.h(TK[j])
                if j > 0:
                    y = bin_list(2 * j)
                    sum = ''
                    for k in range(len(hex(TK[j])[2:])):
                        x = bin_list(int(hex(TK[j])[2:][k], 16))
                        sum = sum + hex(dec_list(mod(multiply_poly(x, y), self.FIELD)))[2:]
                    TK[j] = int(sum, 16)
            # for x in TK:
            #     print(hex(x))
            temp = self.RCON(i)
            # print(hex(temp))
            for x in TK:
                temp = x ^ temp
            #print(hex(temp))
            STK.append(temp)
        return STK

    def encrypt(self, P, KT):
        STK = self.TweakeySchedule(KT)

        temp = P ^ STK[0]
        for i in range(1, self.round + 1):
            temp = self.SubNibbles(temp)
            temp = self.ShiftRows(temp)
            temp = self.MixNibbles(temp)
            temp = temp ^ STK[i]

        return temp

    def decrypt(self, C, KT):
        STK = self.TweakeySchedule(KT)

        temp = C
        for i in range(self.round, 0, -1):
            temp = temp ^ STK[i]
            temp = self.MixNibbles(temp)
            temp = self.Inv_ShiftRows(temp)
            temp = self.Inv_SubNibbles(temp)
        temp = temp ^ STK[0]

        return temp



if __name__ == "__main__":
    m = joltik(128)

    P = 0x0000000000080000
    key = 0x000009000000000000000d0000000000
    C = m.encrypt(P, key)
    print(hex(C))

    C = 0x0000090000000000
    key = 0x0000000001000000000000000e000000
    P = m.decrypt(C, key)
    print(hex(P))