import context
from src.device import Device_Type
from src.host import Host

def test_host():
    h1 = Host("192.168.0.1")
    h2 = Host("192.168.0.2")

    h1.link(h2)
    h2.link(h1)

    assert(h1 == "192.168.0.1")
    assert(h2 == "192.168.0.2")
    assert(h1.device_type() == Device_Type.HOST)
    assert(h2.device_type() == Device_Type.HOST)
    assert(h1.connected_router == h2)
    assert(h2.connected_router == h1)