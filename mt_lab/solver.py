from Pyro4 import expose
from mt19937 import MT19937
import socket
import time


class Solver:
    def __init__(self, workers, input_file_name, output_file_name):
        self.workers = workers
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name

    def solve(self):
        start = time.time()

        print("Workers count:", len(self.workers))

        N, seed = self.read_input()

        # ✅ ЛОКАЛЬНИЙ РЕЖИМ
        if not self.workers:
            mt = MT19937(seed)
            data = [mt.rand_uint32() for _ in range(N)]
            self.write_output(data)
            print("Локальна генерація без PARCS завершена")
            print("Time:", time.time() - start)
            return

        # ✅ PARCS РЕЖИМ
        k = len(self.workers)
        chunk = N // k
        rem = N % k

        mapped = []
        offset = 0

        for i, w in enumerate(self.workers):
            size = chunk + (1 if i < rem else 0)
            mapped.append(
                w.mymap(seed + i * 1000, size, offset)
            )
            offset += size

        result = self.myreduce(mapped, N)
        self.write_output(result)

        print("PARCS генерація завершена")
        print("Time:", time.time() - start)

    @staticmethod
    @expose
    def mymap(seed, size, offset):
        hostname = socket.gethostname()
        print(f"Worker {hostname} | seed={seed} | size={size} | offset={offset}")

        mt = MT19937(seed)
        data = [mt.rand_uint32() for _ in range(size)]
        return {"offset": offset, "data": data}

    @staticmethod
    @expose
    def myreduce(mapped, N):
        result = [0] * N
        for part in mapped:
            d = part.value
            result[d["offset"]: d["offset"] + len(d["data"])] = d["data"]
        return result

    def read_input(self):
        with open(self.input_file_name) as f:
            lines = f.read().split()
        return int(lines[0]), int(lines[1])

    def write_output(self, data):
        with open(self.output_file_name, "w") as f:
            f.write("\n".join(map(str, data)))
