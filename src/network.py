import context
from src.device import Device
from src.router import Router
from src.host import Host
from src.packet import Packet, Packet_Type

class BFS():
    def __init__(self,start:Router,host:Host):
        self.visited = set()
        self.queue = list()
        self.host = host
        self.start = start

    def bfs(self):
        self.queue.append((self.start,self.host))
        
        while len(self.queue) > 0:
            r,p = self.queue.pop(0)

            r.add_forwarding_table_entry(self.host,p)
            self.visited.add(r)

            for r2 in r.get_connected_routers():
                if r2 not in self.visited:
                    self.queue.append((r2,r))

class Network():
    def __init__(self):
        self.routers = dict()
        self.hosts = dict()
        self.devices = dict()
        self.clock = 0
    
    def add_host(self,ip:str):
        self.hosts[ip] = Host(ip)
        self.devices[ip] = self.hosts[ip]
    
    def add_router(self,ip:str):
        self.routers[ip] = Router(ip)
        self.devices[ip] = self.routers[ip]
    
    def link(self,ip1:str,ip2:str):
        self.devices[ip1].link(self.devices[ip2])
        self.devices[ip2].link(self.devices[ip1])
    
    def generate_forwarding_table_entries(self):
        for ip in self.hosts:
            h = self.hosts[ip]
            bfs_obj = BFS(h.get_connected_router(),h)
            bfs_obj.bfs()
    
    def step(self):
        self.clock = self.clock + 1
        print("Tick",self.clock)

        for ip in self.devices:
            self.devices[ip].step()

if __name__ == "__main__":
    net = Network()
    net.add_host("1")
    net.add_host("2")

    net.add_router("3")
    net.add_router("4")

    net.link("1","3")
    net.link("2","4")
    net.link("3","4")

    net.generate_forwarding_table_entries()

    pckt = Packet(123,net.hosts["1"],net.hosts["2"],Packet_Type.DATA)
    pckt2 = Packet(456,net.hosts["2"],net.hosts["1"],Packet_Type.DATA)

    net.hosts["1"].send_pckt(pckt)
    net.hosts["2"].send_pckt(pckt2)

    for i in range(50):
        net.step()