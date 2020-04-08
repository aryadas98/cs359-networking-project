import context
from src.router import Router

def test_router():
    router1 = Router("192.168.0.1")
    router2 = Router("192.168.0.2")
    router3 = Router("192.168.0.3")
    router1.link(router2)
    router1.add_forwarding_table_entry(router3,router2)
    assert(router1.device_type() == "Router")
    assert(router2.device_type() == "Router")
    assert(router3.device_type() == "Router")
    assert(router1.connected_devices == {router2})
    assert(router1.forwarding_table[router2] == router2)
    assert(router1.forwarding_table[router3] == router2)