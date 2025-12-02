import Pyro4
from solver import Solver

ns = Pyro4.locateNS(host="master")

# Автоматично беремо ВСІ воркери
worker_names = ns.list(prefix="parcs.worker")
workers = [Pyro4.Proxy(uri) for uri in worker_names.values()]

print("Workers found:", list(worker_names.keys()))

solver = Solver(
    workers=workers,
    input_file_name="mt_lab/input.txt",
    output_file_name="mt_lab/output.txt"
)

solver.solve()
