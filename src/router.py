import context
from src.device import Device, Device_Type
from src.packet import Packet

class Router(Device):

    def __init__(self,ip,buffer_cap=5):
        super().__init__(ip)
        self.connected_devices = set()
        self.connected_routers = set()
        self.connected_hosts = set()
        self.forwarding_table = dict()

        self.buffer_cap = buffer_cap
        
        self.outgoing_buffer = list()
        self.incoming_buffer = list()
        self.common_buffer = list()
    
    def link(self,dev:Device):
        self.connected_devices.add(dev)
        
        if dev.device_type() == Device_Type.ROUTER:
            self.connected_routers.add(dev)
        elif dev.device_type() == Device_Type.HOST:
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
        return Device_Type.ROUTER

    def receive_pckt(self,pckt:Packet):
        if len(self.incoming_buffer) < self.buffer_cap:
            self.incoming_buffer.append(pckt)
            #print("Router {} received packet {}.".format(self.get_ip(),pckt.get_seg_no()))

    def step(self):
        super().step()

        for p in self.outgoing_buffer:
            t = p.get_to()
            f = self.forwarding_table[t]
            f.receive_pckt(p)
        
        self.outgoing_buffer.clear()

        for p in self.common_buffer:
            self.outgoing_buffer.append(p)
        self.common_buffer.clear()

        for p in self.incoming_buffer:
            self.common_buffer.append(p)
        self.incoming_buffer.clear()

    def __str__(self):
        msg = "Router IP: {}\r\n".format(self.ip)
        msg = msg + "Connected Devices:\r\n"

        for d in self.connected_devices:
            msg = msg + "{}\r\n".format(d.get_ip())
        
        msg = msg + "Forwarding Table:\r\n"

        for k in self.forwarding_table:
            msg = msg + "{} {}\r\n".format(k.get_ip(), self.forwarding_table[k].get_ip())

        return msg