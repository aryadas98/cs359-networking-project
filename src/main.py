import context
from src.networkml import NetworkML

import matplotlib.pyplot as plt
import numpy as np

net = NetworkML()
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

window_data = list()

print("Testing using 3 hosts.")
print("Sending 1500 packets over the network.")
print("Running the simulation for 500 steps.")

for i in range(515):
    net.step()
    
    window_data.append([
        net.hosts["1"].tcp.window_size,
        net.hosts["3"].tcp.window_size,
        net.hosts["6"].tcp.window_size
    ])

window_data = np.array(window_data)

print()
print("Simulation completed.")
print()

print("Mean window size:")
print(np.mean(window_data,axis=0))

plt.figure(figsize=(15,5))
plt.plot(window_data)
plt.title("Window Size")
plt.xlabel("tick")
plt.ylabel("window_size")
plt.legend(['host1','host2','host3'])
plt.show()