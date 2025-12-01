# mt19937.py
W, N, M, R = 32, 624, 397, 31
A = 0x9908B0DF
U, D = 11, 0xFFFFFFFF
S, B = 7, 0x9D2C5680
T, C = 15, 0xEFC60000
L = 18
F = 1812433253

LOWER_MASK = (1 << R) - 1
UPPER_MASK = 0xFFFFFFFF ^ LOWER_MASK


class MT19937:
    def __init__(self, seed=5489):
        self.mt = [0] * N
        self.index = N
        self.seed(seed)

    def seed(self, seed):
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, N):
            self.mt[i] = (F * (self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xFFFFFFFF

    def twist(self):
        for i in range(N):
            x = (self.mt[i] & UPPER_MASK) + (self.mt[(i+1) % N] & LOWER_MASK)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= A
            self.mt[i] = self.mt[(i + M) % N] ^ xA
        self.index = 0

    def rand_uint32(self):
        if self.index >= N:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        y ^= (y >> U)
        y ^= (y << S) & B
        y ^= (y << T) & C
        y ^= (y >> L)

        return y & 0xFFFFFFFF
