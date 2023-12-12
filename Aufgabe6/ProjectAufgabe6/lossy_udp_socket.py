import socket
from threading import Thread
import random


class lossy_udp_socket():
    nBytes=1500
    
    def __init__(self,conn,loc_port,rem_addr,PLR):
        # conn: handler to be called for received packets with function "receive(packet)"
        # loc_port: local port
        # rem_addr: remote address and port pair
        # PLR: received packets are dropped with probability PLR
        self.conn=conn
        self.STOP=False
        self.PLR=PLR
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.settimeout(1.0)
        self.sock.bind(('',loc_port))
        self.addr=rem_addr
        t=Thread(target=self.recv)
        t.start()
        
    # interface for sending packets
    def send(self,packet):
        print('Sending packet with length: '+str(len(packet)))                       
        self.sock.sendto(packet,self.addr)

    # interface for ending socket
    def stop(self):
        self.STOP=True

    # continuously listening for incoming packets
    # filters packets for remote address
    # calls "conn.receive" for received packets
    def recv(self):
        while not self.STOP:
            try:
                packet,addr=self.sock.recvfrom(self.nBytes)
                print('addr= ' + str(addr) + '  selfaddr= ' + str(self.addr))
                if addr == self.addr:
                    if random.random()>self.PLR:
                        print('Received packet with length: '+str(len(packet)))
                        self.conn.receive(packet)
                    else:
                        print('Dropped packet with length: '+str(len(packet)))                       
                else:
                    print('Warning: received packet from remote address'+str(addr))
            except socket.timeout:
                pass
