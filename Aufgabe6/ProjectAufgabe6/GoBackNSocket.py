import time
import random
from threading import Thread
from lossy_udp_socket import lossy_udp_socket

nBytes = 1500
window = 4
global packetNo
global threads
global sendPackets
global receivedPackets
global ackPackets
class GoBackNSocket():

    def __init__(self, port, address):
        self.port = port
        self.address = address

    def receive(self, packet):
        global receivedPackets
        global ackPackets
        string = packet.decode()
        info = string.split(':')
        if len(info) > 3:
            receivedPackets.append([])
            receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])][int(info[1])] = int(info[2])
            receivedPackets[int(info[0])][int(info[1]) + 1] = info[3]
            for x in range(window):
                receivedPackets[int(info[0])].append('')
        elif str(info[0]) == 'ack':
                print('ack:' + info[1] + ':' + info[2])
                if ackPackets.keys().__contains__(int(info[1])) and (int(ackPackets.get(info[1])) == -1 or int(ackPackets.get(info[1])) < int(info[2])):
                    #ackPackets.pop(info[1])
                    ackPackets.update({info[1]: info[2]})
                    print('ack')
                return
        else:
            receivedPackets[int(info[0])].append('')
            receivedPackets[int(info[0])][int(info[1]) + 1] = info[2]
        #print(string)
        #print(receivedPackets)
        bytes = 0
        packet = ''
        for x in receivedPackets[int(info[0])]:
            if type(x) != int:
                bytes += len(x)
                packet += x

        if receivedPackets[int(info[0])][0] == bytes:
            print(packet)
        else:
            print(str(bytes) + ' out of ' + str(receivedPackets[int(info[0])][0]))

        #send ack
        if int(info[1]) == 0:
            lus1.send(('ack:' + info[0] + ':' + info[1]).encode())
        elif ackPackets.__contains__(info[0]):
            if int(ackPackets.get(info[0])) == (int(info[1]) - 1):
                lus1.send(('ack:' + info[0] + ':' + info[1]).encode())

    def send(self, lus, msg):
        global packetNo
        global sendPackets
        global threads
        msg = (str(len(msg))+':').encode() + msg
        threads.append('')
        threads[packetNo] = Thread(target=GoBackNSocket.sendThread(lus, msg, packetNo))
        threads[packetNo].start()
        #sendPackets.append('')
        #sendPackets[packetNo] = msg
        packetNo += 1

    def sendThread(lus, msg, id):
        ackPackets.update({id: -1})
        i = 0
        if len(msg) > nBytes:
            ident = (str(id) + ':' + str(i) + ':').encode()
            start = 0
            stop = nBytes - len(ident)
            dataArr = []
            for x in range(int(len(msg)/nBytes) + 1):
                data = ident + msg[start:stop]
                dataArr.append(data)
                #lus.send(data)
                i += 1
                ident = (str(id) + ':' + str(i)+ ':').encode()
                start = stop
                stop = stop + nBytes - len(ident)
            j = 0
            for x in dataArr:
                while (j - (ackPackets.get(id) + 1)) >= window:
                    pass
                lus.send(x)
                j = j + 1
                time.sleep(1)

    def stop(lus):
        lus.stop()


if __name__ == '__main__':
    port1 = 734
    port2 = 9348
    address1 = ('127.0.0.1', port1)
    address2 = ('127.0.0.2', port2)
    packetNo = 0
    threads = []
    sendPackets = []
    receivedPackets = []
    ackPackets = {}
    gbns1 = GoBackNSocket(port1, address1)
    gbns2 = GoBackNSocket(port2, address2)
    lus1 = lossy_udp_socket(gbns1, port1, address1, 0)
    lus2 = lossy_udp_socket(gbns2, port2, address2, 0)

    print('set up receiver')
    t1 = Thread(target=lus2.recv)
    t1.start()

    t2 = Thread(target=lus1.recv)
    t2.start()

    #with open('Kafka_Der_Prozess.txt', 'r') as file:
    #    msg = file.read()
    with open('test.txt', 'r') as file:
        msg = file.read()
    gbns1.send(lus1, msg.encode())
    #GoBackNSocket.send(lus1, msg.encode())

    time.sleep(1)
    GoBackNSocket.stop(lus1)
    GoBackNSocket.stop(lus2)
    t1.join()
    t2.join()
