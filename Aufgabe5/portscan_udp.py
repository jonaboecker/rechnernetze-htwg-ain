import socket
import threading

# Globale Variable zum Stoppen der Threads
Continue = True


# Funktion zum Scannen eines einzelnen UDP-Ports
def scan_udp(ip, port):
    global Continue
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)  # Timeout für den Socket setzen

        sock.sendto(b'Hallo', (ip, port))  # Datenpaket senden

        data, _ = sock.recvfrom(1024)  # Auf Antwort warten
        if data:
            print(f"Port {port} antwortet")
        sock.close()
    except socket.timeout:
        print(f"Keine Antwort von Port {port}")
        return
    except socket.error as e:
        if e.errno == 10054:
            print(f"Fehlermeldung 10054 von Port {port}")
        return


# Funktion zum Starten der UDP-Scan-Threads
def start_udp_scan(ip, ports):
    threads = []
    for port in ports:
        if not Continue:
            break
        t = threading.Thread(target=scan_udp, args=(ip, port))
        threads.append(t)
        t.start()

    # Auf das Beenden der Threads warten
    for t in threads:
        t.join()


# Beispielaufruf der Funktion mit den gewünschten Parametern
if __name__ == "__main__":
    target_ip = "141.37.168.26"
    target_ports = range(1, 51)
    start_udp_scan(target_ip, target_ports)
