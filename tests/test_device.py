import context
from src.device import DummyDevice

def test_device():
    dev1 = DummyDevice("192.168.0.1")
    dev2 = DummyDevice("172.0.0.1")
    assert(dev1 == "192.168.0.1")
    assert(dev2 == "172.0.0.1")