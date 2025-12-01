import Pyro4
from solver import Solver

ns = Pyro4.locateNS(host="master")

workers = [
    Pyro4.Proxy(ns.lookup("parcs.worker.worker1")),
    Pyro4.Proxy(ns.lookup("parcs.worker.worker2")),
    Pyro4.Proxy(ns.lookup("parcs.worker.worker3")),
    Pyro4.Proxy(ns.lookup("parcs.worker.worker4")),
]

solver = Solver(
    workers=workers,
    input_file_name="mt_lab/input.txt",
    output_file_name="mt_lab/output.txt"
)

solver.solve()
