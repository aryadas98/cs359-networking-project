import context
from src.device import DummyDevice, Device_Type

def test_device():
    dev1 = DummyDevice("192.168.0.1")
    dev2 = DummyDevice("172.0.0.1")
    assert(dev1.device_type() == Device_Type.DUMMY)
    assert(dev2.device_type() == Device_Type.DUMMY)
    assert(dev1 == "192.168.0.1")
    assert(dev2 == "172.0.0.1")