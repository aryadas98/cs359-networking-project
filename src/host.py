import context
from src.device import Device, Device_Type
from src.packet import Packet, Packet_Type

class TCP():
    def __init__(self):
        self.packets_to_send = list()
        self.packets_in_flight = list()
        self.pckts_to_resend = list()
        self.window_size = 1
        self.timeout = 9

class Host(Device):
    def __init__(self, ip:str, buffer_cap=5):
        super().__init__(ip)
        self.connected_router = None
        self.outgoing_buffer = list()
        self.incoming_buffer = list()
        self.buffer_cap = buffer_cap
        self.tcp = TCP()
    
    def link(self,other:Device):
        self.connected_router = other
    
    def get_connected_router(self):
        return self.connected_router
    
    def device_type(self):
        return Device_Type.HOST

    def send_pckt(self,pckt:Packet):
        self.tcp.packets_to_send.append(pckt)

    def receive_pckt(self,pckt:Packet):
        if len(self.incoming_buffer) < self.buffer_cap:
            self.incoming_buffer.append(pckt)
    
    def __str__(self):
        msg = "Host IP: {}\r\n".format(self.ip)
        msg = msg + "Connected to {}\r\n".format(self.connected_router.get_ip())

        return msg
    
    def step(self):
        super().step()

        # handle incoming packets
        for pckt in self.incoming_buffer:
            if pckt.get_pckt_type() == Packet_Type.DATA:
                # send ack packet
                ack_pack = Packet(pckt.get_seg_no(),pckt.get_to(),pckt.get_from(),Packet_Type.ACK)
                self.outgoing_buffer.append(ack_pack)
                print("Host {} received packet {} from host {} and sent ACK.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_from().get_ip()))
            
            elif pckt.get_pckt_type() == Packet_Type.ACK:
                # remove packet from packets in flight and packets to send
                seg_no = pckt.get_seg_no()
                
                index = -1
                for i in range(len(self.tcp.packets_in_flight)):
                    pckt2 = self.tcp.packets_in_flight[i][0]
                    if pckt2.get_seg_no() == seg_no:
                        index = i
                        break
                
                if index >= 0:
                    self.tcp.packets_in_flight.pop(index)
                
                index = -1
                for i in range(len(self.tcp.packets_to_send)):
                    pckt2 = self.tcp.packets_to_send[i][0]
                    if pckt2.get_seg_no() == seg_no:
                        index = i
                        break
                
                if index >= 0:
                    self.tcp.packets_to_send.pop(index)
                
                print("Host {} received ACK from host {}.".format(self.get_ip(), pckt.get_from().get_ip()))

        self.incoming_buffer.clear()

        # resend any timed out packets
        for i in range(len(self.tcp.packets_in_flight)):
            pckt,t = self.tcp.packets_in_flight[i]
            if self.clock - t> self.tcp.timeout:
                self.tcp.pckts_to_resend.append(i)
        
        for i in self.tcp.pckts_to_resend:
            pckt = self.tcp.packets_in_flight[i][0]
            self.tcp.packets_to_send.insert(0,pckt)
            del self.tcp.packets_in_flight[i]
            print("Host {} resending packet {} due to timeout.".format(self.get_ip(),pckt.get_seg_no()))
        
        self.tcp.pckts_to_resend.clear()

        # send packets
        for i in range(self.tcp.window_size):
            if len(self.tcp.packets_to_send) == 0:
                break

            pckt = self.tcp.packets_to_send.pop(0)
            self.outgoing_buffer.append(pckt)
            self.tcp.packets_in_flight.append((pckt,self.clock))

        for pckt in self.outgoing_buffer:
            if pckt.get_pckt_type() == Packet_Type.DATA:
                print("Host {} sent packet {} to host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_to().get_ip()))
            self.connected_router.receive_pckt(pckt)
        
        self.outgoing_buffer.clear()


if __name__ == "__main__":
    h = Host("1")
    h.step()