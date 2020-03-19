import context
from src.packet import Packet, Packet_Type
from src.device import DummyDevice

def test_packet():
    dev1 = DummyDevice("192.168.0.1")
    dev2 = DummyDevice("192.168.0.2")
    pckt = Packet(123,dev1,dev2,Packet_Type.DATA)

    assert(pckt.get_seg_no() == 123)
    assert(pckt.get_from() == dev1)
    assert(pckt.get_to() == dev2)
    assert(pckt.get_pckt_type() == Packet_Type.DATA)