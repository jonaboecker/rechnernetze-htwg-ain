import socket
import struct


def send_request(id, operation, numbers):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    # Verpacken der Nachricht und Senden an den Server
    operation_bytes = operation.encode('utf-8')
    n = len(numbers)
    request = struct.pack(f'I10sB', id, operation_bytes, n) + struct.pack(f'{n}i', *numbers)
    client_socket.send(request)

    # Empfangen der ID und des Ergebnisses vom Server
    response = client_socket.recv(8)
    if len(response) == 8:
        result_id, result_value = struct.unpack('Ii', response)
        print(f"Ergebnis für ID {result_id}: {result_value}")
    else:
        print("Fehlerhafte Antwort erhalten.")

    client_socket.close()


if __name__ == "__main__":
    # Beispielaufruf des Clients
    # op can be: "Summe, Produkt, Maximum, Minimum"
    op = input("Welche Operation soll ausgführt werden? {Summe, Produkt, Maximum, Minimum}: ")
    numbers = []
    while 1:
        user_input = input("Nächste Zahl oder x um zu berechnen: ")
        if not user_input.isdigit():
            break
        numbers.append(int(user_input))
    send_request(123, op, numbers)
