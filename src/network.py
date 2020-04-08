import context
from src.device import Device
from src.router import Router
from src.host import Host

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
        
        for ip in self.routers:
            print(self.routers[ip])
    
    def step(self):
        for ip in self.devices:
            self.devices[ip].step()