import context
from src.device import Device
from src.router import Router
from src.host import Host

class Network():
    def __init__(self):
        self.routers = {}
        self.hosts = {}
        self.devices = {}
    
    def add_host(self,ip:str):
        self.hosts[ip] = Host(ip)
        self.devices[ip] = self.hosts[ip]
    
    def add_router(self,ip:str):
        self.routers[ip] = Router(ip)
        self.devices[ip] = self.routers[ip]
    
    def link(self,ip1:str,ip2:str):
        self.devices[ip1].link(self.devices[ip2])
        self.devices[ip2].link(self.devices[ip1])
    
    def step(self):
        for ip in self.devices:
            self.devices[ip].step()