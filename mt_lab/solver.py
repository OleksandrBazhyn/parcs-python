from Pyro4 import expose

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
    def __init__(self, seed):
        self.mt = [0] * N
        self.index = N
        self.seed(seed)

    def seed(self, seed):
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, N):
            self.mt[i] = (
                F * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i
            ) & 0xFFFFFFFF

    def twist(self):
        for i in range(N):
            x = (self.mt[i] & UPPER_MASK) + (self.mt[(i + 1) % N] & LOWER_MASK)
            xA = x >> 1
            if x & 1:
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

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.workers = workers
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        print("Solver initialized")

    def solve(self):
        print("Job started")
        print("Workers:", len(self.workers))

        total_n, seed = self.read_input()

        k = len(self.workers)
        if k == 0:
            raise RuntimeError("No workers available")

        base = total_n // k
        rest = total_n % k

        mapped = []
        offset = 0

        for i, w in enumerate(self.workers):
            size = base + (1 if i < rest else 0)
            mapped.append(
                w.mymap(seed, size, offset)
            )
            offset += size

        self.write_output(mapped)
        print("Job finished")

    @staticmethod
    @expose
    def mymap(seed, size, offset):
        mt = MT19937(seed)

        for _ in range(offset):
            mt.rand_uint32()

        data = [mt.rand_uint32() for _ in range(size)]

        return {
            "offset": offset,
            "data": data
        }

    def read_input(self):
        with open(self.input_file_name) as f:
            vals = list(map(int, f.read().split()))
        return vals[0], vals[1]

    def write_output(self, mapped):
        total = sum(len(p.value["data"]) for p in mapped)
        result = [0] * total

        for part in mapped:
            block = part.value
            off = block["offset"]
            data = block["data"]
            result[off:off + len(data)] = data

        with open(self.output_file_name, "w") as f:
            for x in result:
                f.write(str(x) + "\n")

        print("Output written")
