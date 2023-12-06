import socket
import struct
import threading


def handle_request(client_socket):
    request_data = client_socket.recv(1024)

    # Überprüfen, ob genügend Daten empfangen wurden
    if len(request_data) < 15:
        return

    request_id, operation, n = struct.unpack('I10sB', request_data[:15])
    operation = operation.decode('utf-8').rstrip('\x00')

    # Überprüfen, ob genügend Daten für die Zahlen empfangen wurden
    expected_data_size = 15 + 4 * n
    if len(request_data) < expected_data_size:
        return

    numbers = struct.unpack(f'{n}i', request_data[15:expected_data_size])

    # Durchführung der Rechenoperation basierend auf dem erhaltenen Befehl
    if operation == 'Summe':
        result = sum(numbers)
        print(f"Summenberechnung: sum {numbers} = {result}")
    elif operation == 'Produkt':
        result = 1
        for num in numbers:
            result *= num
        print(f"Produktberechnung: Produkt {numbers} = {result}")
    elif operation == 'Minimum':
        result = min(numbers)
        print(f"Minimumberechnung: min {numbers} = {result}")
    elif operation == 'Maximum':
        result = max(numbers)
        print(f"Maximumberechnung: max {numbers} = {result}")
    else:
        result = 0  # Unbekannte Operation
        print(f"Unbekannte Operation: res = {result}")

    # Senden des Ergebnisses an den Client
    response = struct.pack('Ii', request_id, result)
    client_socket.send(response)
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)
    print("Server gestartet. Warte auf Verbindung...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Verbunden mit {addr}")

        # Erstellen eines Threads für jeden Client
        client_thread = threading.Thread(target=handle_request, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
