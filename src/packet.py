import context
from src.device import Device
from enum import Enum,auto

class Packet_Type(Enum):
    DATA = auto()
    ACK = auto()

class Packet():
    def __init__(self, seg_no:int, from_device:Device, to_device:Device, pckt_type:Packet_Type):
        self.seg_no = seg_no
        self.from_device = from_device
        self.to_device = to_device
        self.pckt_type = pckt_type
    
    def get_seg_no(self):
        return self.seg_no
    
    def get_from(self):
        return self.from_device
    
    def get_to(self):
        return self.to_device
    
    def get_pckt_type(self):
        return self.pckt_type

    def __str__(self):
        return "From: {} To: {} Seg_No: {} Type: {}".format(self.from_device, self.to_device, self.seg_no, self.pckt_type)