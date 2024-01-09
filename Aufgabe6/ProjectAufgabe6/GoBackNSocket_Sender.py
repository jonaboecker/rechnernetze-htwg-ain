import threading
import time
from threading import Thread
from lossy_udp_socket import lossy_udp_socket

nBytes = 500
window = 4
global packetNo
global threads
global ackPackets
global timer_expired
global message_complete
global last_expected_ack


class GoBackNSocket:

    def __init__(self, port, address):
        self.port = port
        self.address = address

    @staticmethod
    def receive(packet):
        global ackPackets
        global message_complete
        global last_expected_ack
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
                    if packet_number == last_expected_ack:
                        message_complete[int(info[1])] = True

    def send(self, lus, msg):
        global packetNo
        global threads
        msg = (str(len(msg))+':').encode() + msg
        threads.append('')
        threads[packetNo] = Thread(target=GoBackNSocket.send_thread(self, lus, msg, packetNo))
        threads[packetNo].start()
        packetNo += 1

    def send_thread(self, lus, msg, id):
        global message_complete
        global last_expected_ack
        message_complete.append('')
        message_complete[id] = False
        ackPackets.update({str(id): -1})
        i = 0
        global timer_expired
        timer_expired = False
        if len(msg) > 0:
            ident = (str(id) + ':' + str(i) + ':').encode()
            start = 0
            stop = nBytes - len(ident)
            data_arr = []
            for x in range(int(len(msg)/nBytes) + 1):
                data = ident + msg[start:stop]
                data_arr.append(data)
                i += 1
                ident = (str(id) + ':' + str(i) + ':').encode()
                start = stop
                stop = stop + nBytes - len(ident)
            last_expected_ack = len(data_arr) - 1
            j = 0
            while message_complete[id] is False:
                if timer_expired is True:
                    timer_expired = False
                    j = int(ackPackets.get(str(id))) + 1
                    self.timer(self, 2)
                    continue
                while len(data_arr) > j:
                    while (j - (int(ackPackets.get(str(id))) + 1)) >= window and timer_expired is False:
                        pass
                    if timer_expired is True:
                        timer_expired = False
                        j = int(ackPackets.get(str(id))) + 1
                        self.timer(self, 2)
                        continue

                    lus.send(data_arr[j])
                    self.timer(self, 1)
                    j += 1
                    time.sleep(0.01)

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

if __name__ == '__main__':
    port1 = 8888
    address1 = ('127.0.0.1', 8889)
    
    packetNo = 0
    threads = []
    ackPackets = {}
    message_complete = []

    gbns1 = GoBackNSocket(port1, address1)
    lus1 = lossy_udp_socket(gbns1, port1, address1, 0.1)

    with open('test.txt', 'r') as file:
        msg = file.read()

    gbns1.send(lus1, msg.encode())
    gbns1.send(lus1, 'hallo'.encode())
    gbns1.stop(lus1)