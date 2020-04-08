import context
from src.host import Host
from src.router import Router
from src.network import Network

def test_network():
    net = Network()
    net.add_host("192.168.0.1")
    net.add_host("192.168.0.2")
    net.add_router("192.168.0.3")
    net.add_router("192.168.0.4")

    net.link("192.168.0.1","192.168.0.3")
    net.link("192.168.0.2","192.168.0.4")
    net.link("192.168.0.3","192.168.0.4")

    net.generate_forwarding_table_entries()

    assert("192.168.0.1" in net.hosts)
    assert("192.168.0.2" in net.hosts)
    assert("192.168.0.3" in net.routers)
    assert("192.168.0.4" in net.routers)

    assert("192.168.0.1" in net.routers["192.168.0.3"].connected_devices)
    assert("192.168.0.4" in net.routers["192.168.0.3"].connected_devices)
    assert("192.168.0.2" in net.routers["192.168.0.4"].connected_devices)
    assert("192.168.0.3" in net.routers["192.168.0.4"].connected_devices)

    assert(net.routers["192.168.0.3"].forwarding_table["192.168.0.1"] == "192.168.0.1")
    assert(net.routers["192.168.0.3"].forwarding_table["192.168.0.4"] == "192.168.0.4")
    assert(net.routers["192.168.0.3"].forwarding_table["192.168.0.2"] == "192.168.0.4")
    assert(net.routers["192.168.0.4"].forwarding_table["192.168.0.2"] == "192.168.0.2")
    assert(net.routers["192.168.0.4"].forwarding_table["192.168.0.3"] == "192.168.0.3")
    assert(net.routers["192.168.0.4"].forwarding_table["192.168.0.1"] == "192.168.0.3")
    