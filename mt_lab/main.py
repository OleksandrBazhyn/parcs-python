import Pyro4
from solver import Solver

# Підключення до Name Server
ns = Pyro4.locateNS()

# ✅ 4 ВОРКЕРИ
workers = [
    Pyro4.Proxy(ns.lookup("parcs.worker")),
    Pyro4.Proxy(ns.lookup("parcs.worker")),
    Pyro4.Proxy(ns.lookup("parcs.worker")),
    Pyro4.Proxy(ns.lookup("parcs.worker"))
]

solver = Solver(
    workers=workers,
    input_file_name="mt_lab/input.txt",
    output_file_name="mt_lab/output.txt"
)

solver.solve()
