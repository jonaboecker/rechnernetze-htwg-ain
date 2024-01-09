import threading
import time
from threading import Thread
from lossy_udp_socket import lossy_udp_socket

nBytes = 500
window = 4
global packetNo
global threads
global sendPackets
global receivedPackets
global ackPackets
global timer_expired
global message_complete


class GoBackNSocket:

    def __init__(self, port, address):
        self.port = port
        self.address = address

    @staticmethod
    def receive(packet):
        global receivedPackets
        global ackPackets
        global message_complete
        string = packet.decode()
        info = string.split(':')
        print(info)

        if str(info[0]) == 'ack':  # ack message
            ack_number = ackPackets.get(info[1])
            packet_number = int(info[2])
            if ack_number is not None and packet_number is not None:
                if ack_number == -1 or ack_number < packet_number:
                    ackPackets.update({info[1]: packet_number})
                    print('ack:' + info[1] + ':' + info[2])
            return

        # send ack
        if int(info[1]) == 0:
            lus1.send(('ack:' + info[0] + ':' + info[1]).encode())
            ackPackets.update({info[0]: info[1]})
        elif ackPackets.__contains__(info[0]):
            if int(ackPackets.get(info[0])) == (int(info[1]) - 1):
                lus1.send(('ack:' + info[0] + ':' + info[1]).encode())
                ackPackets.update({info[0]: info[1]})
            else:
                return
        else:
            return

        if len(info) > 3:   # first message
            if len(receivedPackets) <= int(info[0]):
                receivedPackets.append([])
            receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])][int(info[1])] = int(info[2])
            receivedPackets[int(info[0])][int(info[1]) + 1] = info[3]
            for x in range(window):
                receivedPackets[int(info[0])].append('')
        else:       # follow-up message
            if len(receivedPackets) <= int(info[0]):
                receivedPackets.append([])
            while len(receivedPackets[int(info[0])]) <= int(info[1]) + 1:
                receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])][int(info[1]) + 1] = info[2]
        # print(string)
        # print(receivedPackets)
        bytes = 0
        packet = ''
        for x in receivedPackets[int(info[0])]:
            if type(x) is not int:
                bytes += len(x)
                packet += x

        if receivedPackets[int(info[0])][0] == bytes:
            print(packet)
        else:
            print(str(bytes) + ' out of ' + str(receivedPackets[int(info[0])][0]))

    @staticmethod
    def timer(self, s):
        threading.Timer(s, self.timer_trigger).start()

    @staticmethod
    def timer_trigger():
        global timer_expired
        timer_expired = True

    @staticmethod
    def stop(lus):
        lus.stop()

def receiver_thread():
    t1 = Thread(target=lus1.recv)
    t1.start()

if __name__ == '__main__':
    port2 = 8889
    address2 = ('127.0.0.1', 8888)
    
    packetNo = 0
    threads = []
    receivedPackets = []
    ackPackets = {}
    message_complete = []

    gbns2 = GoBackNSocket(port2, address2)
    lus1 = lossy_udp_socket(gbns2, port2, address2, 0.1)

    receiver_thread()

"""if __name__ == '__main__':
    port1 = 734
    port2 = 9348
    address1 = ('127.0.0.1', port1)
    address2 = ('127.0.0.2', port2)
    packetNo = 0
    threads = []
    sendPackets = []
    receivedPackets = []
    ackPackets = {}
    message_complete = []
    gbns1 = GoBackNSocket(port1, address1)
    gbns2 = GoBackNSocket(port2, address2)
    lus1 = lossy_udp_socket(gbns1, port1, address1, 0.2)
    lus2 = lossy_udp_socket(gbns2, port2, address2, 0.2)

    print('set up receiver')
    t1 = Thread(target=lus2.recv)
    t1.start()

    t2 = Thread(target=lus1.recv)
    t2.start()

    with open('test.txt', 'r') as file:
        msg = file.read()
    gbns1.send(lus1, msg.encode())
    gbns1.send(lus1, 'hallo'.encode())
    # GoBackNSocket.send(lus1, msg.encode())

    GoBackNSocket.stop(lus1)
    GoBackNSocket.stop(lus2)
    t1.join()
    t2.join()"""
