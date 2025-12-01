import Pyro4
import socket
from solver import Solver

host = socket.gethostname()   # ✅ worker1 / worker2 / worker3 / worker4

daemon = Pyro4.Daemon(host=host)
ns = Pyro4.locateNS(host="master")

uri = daemon.register(Solver)
ns.register("parcs.worker." + host, uri)

print(f"✅ Worker registered as parcs.worker.{host}")

daemon.requestLoop()
