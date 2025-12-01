import Pyro4
import socket
from mt19937 import MT19937

@Pyro4.expose
class Worker:
    def mymap(self, seed, size, offset):
        hostname = socket.gethostname()
        print(f"🟢 Worker {hostname} | seed={seed} | size={size} | offset={offset}")

        mt = MT19937(seed)
        data = [mt.rand_uint32() for _ in range(size)]

        return {"offset": offset, "data": data}


host = socket.gethostname()

daemon = Pyro4.Daemon(host=host)
ns = Pyro4.locateNS(host="master")

uri = daemon.register(Worker)   # ✅ РЕЄСТРУЄМО НЕ SOLVER!
ns.register("parcs.worker." + host, uri)

print(f"✅ Worker registered as parcs.worker.{host}")

daemon.requestLoop()
