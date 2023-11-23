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

    def TweakeySchedule(self, KT, r):
        s = hex(KT)[2:]
        while len(s) < self.s * 16:
            s = '0' + s

        TK = []
        for i in range(self.s):
            TK.append(int(s[i * 16:(i + 1) * 16], 16))

        STK = []
        temp = self.RCON(1)
        for x in TK:
            temp = x ^ temp
        STK.append(temp)

        for i in range(2, r + 1):
            for j in range(self.s):
                TK[j] = self.h(TK[j])
                if j > 0:
                    y = bin_list(2 * j)
                    sum = ''
                    for k in range(len(hex(TK[j])[2:])):
                        x = bin_list(int(hex(TK[j])[2:][k], 16))
                        sum = sum + hex(dec_list(mod(multiply_poly(x, y), self.FIELD)))[2:]
                    TK[j] = int(sum, 16)
            temp = self.RCON(i)
            for x in TK:
                temp = x ^ temp
            STK.append(temp)
        return STK

    def Inv_Tweakey(self, KT, r):
        s = hex(KT)[2:]
        while len(s) < self.s * 16:
            s = '0' + s

        TK = []
        for i in range(self.s):
            TK.append(int(s[i * 16:(i + 1) * 16], 16))
        F = [9, 13]

        for i in range(r):
            for j in range(self.s):
                if j > 0:
                    y = bin_list(F[j - 1])
                    sum = ''
                    for k in range(len(hex(TK[j])[2:])):
                        x = bin_list(int(hex(TK[j])[2:][k], 16))
                        sum = sum + hex(dec_list(mod(multiply_poly(x, y), self.FIELD)))[2:]
                    TK[j] = int(sum, 16)
                TK[j] = self.Inv_h(TK[j])
        key = ''
        for i in range(self.s):
            s = hex(TK[i])[2:]
            while len(s) < 16:
                s = '0' + s
            key = key + s
#        print("lower key difference:", key)

        return int(key, 16)

    def diff_encrypt(self, temp, KT, r):
        STK = self.TweakeySchedule(KT, r[0] + r[1])
        for i in range(r[1]):
            temp = self.SubNibbles(temp)
            temp = self.ShiftRows(temp)
            temp = self.MixNibbles(temp)
            temp = temp ^ STK[r[0] + i]
        return temp

    def diff_decrypt(self, temp, KT, r):
        STK = self.TweakeySchedule(KT, r[0] + r[1])

        for i in range(r[1]):
            temp = temp ^ STK[r[0] + i]
            temp = self.MixNibbles(temp)
            temp = self.Inv_ShiftRows(temp)
            temp = self.Inv_SubNibbles(temp)
        return temp

    def boomerang(self, r, N3, dp, dc, uk, lk):
        sum = 0

        key = ''.join([random.choice('0123456789abcdef') for i in range(32)])
        key = int(key, 16)

        for i in range(N3):
            p1 = int(''.join([random.choice('0123456789abcdef') for i in range(16)]), 16)
            p2 = p1 ^ dp

            c1 = self.diff_encrypt(p1, key, r)
            c2 = self.diff_encrypt(p2, key ^ uk, r)

            c3 = c1 ^ dc
            c4 = c2 ^ dc

            p3 = self.diff_decrypt(c3, key ^ lk, r)
            p4 = self.diff_decrypt(c4, key ^ uk ^ lk, r)

            if p3 ^ p4 == dp: sum = sum + 1

        return sum

    def send_boomerangs(self, r, N1, N2, N3, dp, dc, uk, lk):
        NUM = []
        for i in range(N1):
            sum = 0
            for j in range(N2):
                sum = sum + self.boomerang(r, N3, dp, dc, uk, lk)
            NUM.append(sum)
        sum = 0
        for i in range(N1):
            sum = sum + NUM[i]
        print(sum)
        if sum == 0:
            print("no trail!")
        else:
            print(log2(N1 * N2 * N3 / sum))
        return sum


if __name__ == "__main__":
    r = [4, 1, 3]
    m = joltik(128)

    dp = 0x000D000020000000
    dc = 0x0000000290000000

    uk = 0x00000000000006000000000000000600
    lk = 0x00000000090000000000000009000000

    lk = m.Inv_Tweakey(lk, r[0] + r[1])
    print(hex(lk))

    #m.send_boomerangs(r, 16, 2**5, 2**5, dp, dc, uk, lk)