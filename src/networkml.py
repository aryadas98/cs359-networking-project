import context
from src.device import Device
from src.router import Router
from src.hostml import HostML
from src.packet import Packet, Packet_Type

class BFSML():
    def __init__(self,start:Router,host:HostML):
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

class NetworkML():
    def __init__(self):
        self.routers = dict()
        self.hosts = dict()
        self.devices = dict()
        self.clock = 0
    
    def add_host(self,ip:str,buffer_cap=5):
        self.hosts[ip] = HostML(ip,buffer_cap)
        self.devices[ip] = self.hosts[ip]
    
    def add_router(self,ip:str,buffer_cap=5):
        self.routers[ip] = Router(ip,buffer_cap)
        self.devices[ip] = self.routers[ip]
    
    def link(self,ip1:str,ip2:str):
        self.devices[ip1].link(self.devices[ip2])
        self.devices[ip2].link(self.devices[ip1])
    
    def generate_forwarding_table_entries(self):
        for ip in self.hosts:
            h = self.hosts[ip]
            bfs_obj = BFSML(h.get_connected_router(),h)
            bfs_obj.bfs()
    
    def step(self):
        self.clock = self.clock + 1
        # print("Tick",self.clock)

        for ip in self.routers:
            self.devices[ip].step()

        for ip in self.hosts:
            self.devices[ip].step()