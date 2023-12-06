import socket
import base64
import os

def encode_base64(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

server = 'asmtp.htwg-konstanz.de'
port = 587

# Verbindung aufbauen
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))
recv = client_socket.recv(1024).decode()
print(recv)

# Benutzerdaten
username = input("Geben Sie Ihren Benutzernamen ein: ")
password = input("Geben Sie Ihr Passwort ein: ")

# Authentifizierung
auth_message = "AUTH LOGIN\r\n"
client_socket.send(auth_message.encode())
recv_auth = client_socket.recv(1024).decode()
print(recv_auth)

encoded_username = encode_base64(username)
encoded_password = encode_base64(password)

client_socket.send((encoded_username + "\r\n").encode())
recv_user = client_socket.recv(1024).decode()
print(recv_user)

client_socket.send((encoded_password + "\r\n").encode())
recv_pass = client_socket.recv(1024).decode()
print(recv_pass)

# E-Mail-Daten eingeben
from_address = input("Geben Sie die Absenderadresse ein: ")
to_address = input("Geben Sie die Empfängeradresse ein: ")
fake_from_address = "From: " + input("Geben Sie die Fake-Absenderadresse ein: ")
fake_to_address = "To: " + input("Geben Sie die Fake-Empfängeradresse ein: ")
fake_date = "Date: " + input("Geben Sie ein Fake-Datum ein: {Thu, 30 Nov 2023}") + " 13:10:50 +0100"
subject = "Subject:" + input("Geben Sie den Betreff ein: ")
body = input("Geben Sie die Nachricht ein: ")

# E-Mail senden
client_socket.send(f"MAIL FROM: <{from_address}>\r\n".encode())
recv_from = client_socket.recv(1024).decode()
print(recv_from)

client_socket.send(f"RCPT TO: <{to_address}>\r\n".encode())
recv_to = client_socket.recv(1024).decode()
print(recv_to)

client_socket.send("DATA\r\n".encode())
recv_data = client_socket.recv(1024).decode()
print(recv_data)

message = f"{fake_from_address}\r\n{fake_to_address}\r\n{subject}\r\n{fake_date}\r\n\r\n{body}\r\n.\r\n"
client_socket.send(message.encode())
recv_msg = client_socket.recv(1024).decode()
print(recv_msg)

# Verbindung schließen
client_socket.send("QUIT\r\n".encode())
client_socket.close()
