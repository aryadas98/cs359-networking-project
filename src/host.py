import context
from src.device import Device

class Host(Device):
    def __init__(self, ip:str):
        super().__init__(ip)
        self.connected_router = None
    
    def link(self,other:Device):
        self.connected_router = other
    
    def __str__(self):
        msg = "Host IP: {}\r\n".format(self.ip)
        msg = msg + "Connected to {}\r\n".format(self.connected_router.get_ip())

        return msg
    
    def step(self):
        pass