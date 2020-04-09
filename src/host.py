import context
from src.device import Device, Device_Type
from src.packet import Packet

class Host(Device):
    def __init__(self, ip:str, buffer_cap=5):
        super().__init__(ip)
        self.connected_router = None
        self.outgoing_buffer = list()
        self.incoming_buffer = list()
        self.buffer_cap = buffer_cap
    
    def link(self,other:Device):
        self.connected_router = other
    
    def get_connected_router(self):
        return self.connected_router
    
    def device_type(self):
        return Device_Type.HOST

    def send_pckt(self,pckt:Packet):
        if len(self.outgoing_buffer) < self.buffer_cap:
            self.outgoing_buffer.append(pckt)

    def receive_pckt(self,pckt:Packet):
        if len(self.incoming_buffer) < self.buffer_cap:
            self.incoming_buffer.append(pckt)
    
    def __str__(self):
        msg = "Host IP: {}\r\n".format(self.ip)
        msg = msg + "Connected to {}\r\n".format(self.connected_router.get_ip())

        return msg
    
    def step(self):
        for pckt in self.incoming_buffer:
            print("Host {} received packet {} from host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_from().get_ip()))
        
        self.incoming_buffer.clear()

        for pckt in self.outgoing_buffer:
            print("Host {} sent packet {} to host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_to().get_ip()))
            self.connected_router.receive_pckt(pckt)
        
        self.outgoing_buffer.clear()