from threading import Thread
from lossy_udp_socket import lossy_udp_socket

class GoBackNSocket():
    def receive(packet):
        print('packet recived')
        print(packet.decode())

    def send(lus, msg):
        lus.send(msg)

    def stop(lus):
        lus.stop()


if __name__ == '__main__':
    port1 = 734
    port2 = 9348
    address1 = ('127.0.0.1', port1)
    address2 = ('127.0.0.2', port2)
    lus1 = lossy_udp_socket(GoBackNSocket, port1, address1, 0)
    lus2 = lossy_udp_socket(GoBackNSocket, port2, address2, 0)

    print('set up reciver')
    t1 = Thread(target=lus2.recv)
    t1.start()

    print('send hallo')
    with open('Kafka_Der_Prozess.txt', 'r') as file:
        msg = file.read()
    GoBackNSocket.send(lus1, msg.encode())

    GoBackNSocket.stop(lus1)
    GoBackNSocket.stop(lus2)
    t1.join()
