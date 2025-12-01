import Pyro4
from solver import Solver

Pyro4.Daemon.serveSimple(
    {
        Solver: "parcs.worker"
    },
    host="0.0.0.0",
    port=50000,
    ns=True
)
