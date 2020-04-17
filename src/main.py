import context
from src.network import Network

net = Network()
net.add_host("1",16)
net.add_host("2",16)
net.add_host("3",16)
net.add_host("4",16)
net.add_host("6",16)
net.add_host("7",16)

net.add_router("5",16)

net.link("1","5")
net.link("2","5")
net.link("3","5")
net.link("4","5")
net.link("6","5")
net.link("7","5")

net.generate_forwarding_table_entries()

for i in range(500):
    net.hosts["1"].send_random_packet(net.hosts["2"])

for i in range(500):
    net.hosts["3"].send_random_packet(net.hosts["4"])

for i in range(500):
    net.hosts["6"].send_random_packet(net.hosts["7"])

for i in range(515):
    net.step()
    print(
       net.hosts["1"].tcp.window_size,
       net.hosts["3"].tcp.window_size, 
       net.hosts["6"].tcp.window_size)