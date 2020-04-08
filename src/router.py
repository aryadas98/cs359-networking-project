import context
from src.device import Device

class Router(Device):

    def __init__(self,ip):
        super().__init__(ip)
        self.connected_devices = set()
        self.connected_routers = set()
        self.connected_hosts = set()
        self.forwarding_table = dict()
    
    def link(self,dev:Device):
        self.connected_devices.add(dev)
        
        if dev.device_type() == "Router":
            self.connected_routers.add(dev)
        elif dev.device_type() == "Host":
            self.connected_hosts.add(dev)

        self.add_forwarding_table_entry(dev,dev)

    def get_connected_devices(self):
        return self.connected_devices
    
    def get_connected_routers(self):
        return self.connected_routers
    
    def get_connected_hosts(self):
        return self.connected_hosts

    def add_forwarding_table_entry(self, dest:Device, forward_to:Device):
        self.forwarding_table[dest] = forward_to
    
    def device_type(self):
        return "Router"

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