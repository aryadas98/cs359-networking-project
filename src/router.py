import context
from src.device import Device

class Router(Device):

    def __init__(self,ip):
        super().__init__(ip)
        self.connected_devices = []
        self.forwarding_table = {}
    
    def link(self,dev:Device):
        self.connected_devices.append(dev)
        self.add_forwarding_table_entry(dev,dev)
    
    def add_forwarding_table_entry(self, dest:Device, forward_to:Device):
        self.forwarding_table[dest] = forward_to
    
    def step(self):
        pass

    def __str__(self):
        msg = "Router IP: {}\r\n".format(self.ip)
        msg = msg + "Connected Devices:\r\n"

        for d in self.connected_devices:
            msg = msg + "{}\r\n".format(d.get_ip())
        
        msg = msg + "Forwarding Table:\r\n"

        for k in self.forwarding_table:
            msg = msg + "{} {}\r\n".format(k.get_ip(), self.forwarding_table[k].get_ip())

        return msg