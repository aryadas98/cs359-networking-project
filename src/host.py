import context
from src.device import Device, Device_Type
from src.packet import Packet, Packet_Type

class TCP():
    def __init__(self):
        self.packets_to_send = list()
        self.packets_in_flight = list()
        self.pckts_to_resend = list()
        self.window_size = 1
        self.ssthresh = 18
        self.timeout = 10

        self.ack_recv_flag = False
        self.ack_timeout_flag = False

class Host(Device):
    def __init__(self, ip:str, buffer_cap=5):
        super().__init__(ip)
        self.connected_router = None
        self.outgoing_buffer = list()
        self.incoming_buffer = list()
        self.buffer_cap = buffer_cap
        self.tcp = TCP()
        self.def_seg_no = 1
    
    def link(self,other:Device):
        self.connected_router = other
    
    def get_connected_router(self):
        return self.connected_router
    
    def device_type(self):
        return Device_Type.HOST

    def send_pckt(self,pckt:Packet):
        self.tcp.packets_to_send.append(pckt)
    
    def send_random_packet(self,to_device:Device):
        pckt = Packet(self.def_seg_no,self,to_device,Packet_Type.DATA)
        self.send_pckt(pckt)
        self.def_seg_no = self.def_seg_no + 1

    def receive_pckt(self,pckt:Packet):
        if len(self.incoming_buffer) < self.buffer_cap:
            self.incoming_buffer.append(pckt)
    
    def __str__(self):
        msg = "Host IP: {}\r\n".format(self.ip)
        msg = msg + "Connected to {}\r\n".format(self.connected_router.get_ip())

        return msg
    
    def step(self):
        super().step()

        self.tcp.ack_recv_flag = False
        self.tcp.ack_timeout_flag = False

        # handle incoming packets
        for pckt in self.incoming_buffer:
            if pckt.get_pckt_type() == Packet_Type.DATA:
                # send ack packet
                ack_pack = Packet(pckt.get_seg_no(),pckt.get_to(),pckt.get_from(),Packet_Type.ACK)
                self.outgoing_buffer.append(ack_pack)
                # print("Host {} received packet {} from host {} and sent ACK.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_from().get_ip()))
                pass
            
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
                    self.tcp.timeout = self.clock-self.tcp.packets_in_flight[i][1]     # set tcp timeout adaptively
                    self.tcp.packets_in_flight.pop(index)
                
                index = -1
                for i in range(len(self.tcp.packets_to_send)):
                    pckt2 = self.tcp.packets_to_send[i]
                    if pckt2.get_seg_no() == seg_no:
                        index = i
                        break
                
                if index >= 0:
                    self.tcp.packets_to_send.pop(index)
                
                # print("Host {} received ACK from host {}.".format(self.get_ip(), pckt.get_from().get_ip()))
                self.tcp.ack_recv_flag = True
                pass

        self.incoming_buffer.clear()

        # resend any timed out packets
        for i in range(len(self.tcp.packets_in_flight)):
            pckt,t = self.tcp.packets_in_flight[i]
            if self.clock - t> self.tcp.timeout:
                self.tcp.pckts_to_resend.append(i)
        
        for i in self.tcp.pckts_to_resend:
            pckt = self.tcp.packets_in_flight[i][0]
            self.tcp.packets_to_send.insert(0,pckt)
            # print("Host {} resending packet {} due to timeout.".format(self.get_ip(),pckt.get_seg_no()))
            pass
        
        for i in sorted(self.tcp.pckts_to_resend,reverse=True):
            del self.tcp.packets_in_flight[i]

        # reset window size and ssthresh in case of timeout
        if len(self.tcp.pckts_to_resend) > 0:
            self.tcp.ack_timeout_flag = True

        if self.tcp.ack_timeout_flag:
            self.tcp.ssthresh = self.tcp.window_size
            self.tcp.window_size = self.tcp.ssthresh//2
        elif self.tcp.ack_recv_flag:
            if self.tcp.window_size < self.tcp.ssthresh//4:
                self.tcp.window_size = self.tcp.window_size * 2  # slow start
            elif self.tcp.window_size < self.tcp.ssthresh//2:
                self.tcp.window_size = self.tcp.ssthresh//2
            else:
                self.tcp.window_size = self.tcp.window_size + 1  # linear increase

        self.tcp.pckts_to_resend.clear()

        if self.tcp.window_size < 1:
            self.tcp.window_size = 1    # minimum window size
        
        if self.tcp.ssthresh < 2:
            self.tcp.ssthresh = 2   # minimum ssthresh value

        # send packets
        # send packets only if there are no packets in flight
        if len(self.tcp.packets_in_flight) == 0:

            for i in range(self.tcp.window_size):
                if len(self.tcp.packets_to_send) == 0:
                    break

                pckt = self.tcp.packets_to_send.pop(0)
                self.outgoing_buffer.append(pckt)
                self.tcp.packets_in_flight.append((pckt,self.clock))

            for pckt in self.outgoing_buffer:
                if pckt.get_pckt_type() == Packet_Type.DATA:
                    # print("Host {} sent packet {} to host {}.".format(self.get_ip(), pckt.get_seg_no(), pckt.get_to().get_ip()))
                    pass
                self.connected_router.receive_pckt(pckt)
            
            self.outgoing_buffer.clear()


if __name__ == "__main__":
    h = Host("1")
    h.step()