import context
from abc import ABC,abstractclassmethod

class Device(ABC):
    
    def __init__(self, ip:str):
        self.ip = ip
    
    def get_ip(self):
        return self.ip
    
    def __eq__(self,other):
        if isinstance(other,str):
            return self.ip == other
        else:
            return self.ip == other.ip

    def __hash__(self):
        return hash(self.ip)
    
    @abstractclassmethod
    def device_type(self):
        pass

    @abstractclassmethod
    def link(self,other):
        pass

    @abstractclassmethod
    def receive_pckt(self,pckt):
        pass

    @abstractclassmethod
    def step(self):
        pass

    @abstractclassmethod
    def __str__(self):
        pass

# use this class for testing
class DummyDevice(Device):
    def __init__(self, ip:str):
        super().__init__(ip)
    
    def device_type(self):
        return "Dummy"

    def link(self,other):
        pass

    def __str__(self):
        return "Device IP: {}".format(self.ip)
    
    def receive_pckt(self,pckt):
        pass
    
    def step(self):
        pass