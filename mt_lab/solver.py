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

        # ❌ Забороняємо локальний режим для лабораторної
        if not self.workers:
            raise RuntimeError("❌ Workers не підключені! PARCS не працює!")

        # ✅ PARCS РОЗБИТТЯ
        k = len(self.workers)
        chunk = N // k
        rem = N % k

        mapped = []
        offset = 0

        for i, w in enumerate(self.workers):
            size = chunk + (1 if i < rem else 0)

            print(f"➡️ Send task to worker {i+1} | size={size} | offset={offset}")

            mapped.append(
                w.mymap(seed + i * 1000, size, offset)
            )

            offset += size

        # ✅ ЗБІР РЕЗУЛЬТАТІВ
        result = self.myreduce(mapped, N)

        self.write_output(result)

        print("✅ PARCS генерація завершена")
        print("⏱ Time:", time.time() - start)

    @staticmethod
    @expose
    def mymap(seed, size, offset):
        hostname = socket.gethostname()
        print(f"🟢 Worker {hostname} | seed={seed} | size={size} | offset={offset}")

        mt = MT19937(seed)
        data = [mt.rand_uint32() for _ in range(size)]

        return {"offset": offset, "data": data}

    @staticmethod
    @expose
    def myreduce(self, parts, N):
        result = [0] * N

        for part in parts:
            offset = part["offset"]
            data = part["data"]

            for i in range(len(data)):
                result[offset + i] = data[i]

        return result

    def read_input(self):
        with open(self.input_file_name) as f:
            lines = f.read().split()
        return int(lines[0]), int(lines[1])

    def write_output(self, data):
        with open(self.output_file_name, "w") as f:
            f.write("\n".join(map(str, data)))
