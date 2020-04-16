import context
from src.network import Network

net = Network()
net.add_host("1",5)
net.add_host("2",5)

net.add_router("3",5)
net.add_router("4",5)

net.link("1","3")
net.link("2","4")
net.link("3","4")

net.generate_forwarding_table_entries()

for i in range(100):
    net.hosts["1"].send_random_packet(net.hosts["2"])

for i in range(315):
    net.step()