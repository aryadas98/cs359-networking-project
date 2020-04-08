import context
from src.device import Device
from src.packet import Packet

class Host(Device):
    def __init__(self, ip:str):
        super().__init__(ip)
        self.connected_router = None
    
    def link(self,other:Device):
        self.connected_router = other
    
    def get_connected_router(self):
        return self.connected_router
    
    def device_type(self):
        return "Host"

    def send_pckt(self,pckt:Packet):
        print("Host {} sent packet {} to host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_to().get_ip()))
        self.connected_router.receive_pckt(pckt)

    def receive_pckt(self,pckt:Packet):
        print("Host {} received packet {} from host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_from().get_ip()))
    
    def __str__(self):
        msg = "Host IP: {}\r\n".format(self.ip)
        msg = msg + "Connected to {}\r\n".format(self.connected_router.get_ip())

        return msg
    
    def step(self):
        pass