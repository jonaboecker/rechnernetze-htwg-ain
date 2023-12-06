import socket
import threading

# Globale Variable zum Stoppen der Threads
Continue = True


# Funktion zum Scannen eines einzelnen TCP-Ports
def scan_tcp(ip, port):
    global Continue
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout für die Verbindung setzen

        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} offen")
        sock.close()
    except KeyboardInterrupt:
        Continue = False
        return
    except socket.error:
        print("Fehler beim Verbinden")
        return


# Funktion zum Starten der Threads
def start_tcp_scan(ip, ports):
    threads = []
    for port in ports:
        if not Continue:
            break
        t = threading.Thread(target=scan_tcp, args=(ip, port))
        threads.append(t)
        t.start()

    # Auf das Beenden der Threads warten
    for t in threads:
        t.join()


# Beispielaufruf der Funktion mit den gewünschten Parametern
if __name__ == "__main__":
    target_ip = "141.37.168.26"
    target_ports = range(1, 51)
    start_tcp_scan(target_ip, target_ports)
