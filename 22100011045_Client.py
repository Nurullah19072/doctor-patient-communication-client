#22100011045 - Nurullah Yıldırım

import socket
import sys
import threading
import time

HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024

if len(sys.argv) != 3:
    print("Kullanım: python OgrNo_Client.py [Doktor/Hasta] [TCP/UDP]")
    sys.exit(1)

user_type = sys.argv[1]
connection_type = sys.argv[2]

assigned_name = None  # Hasta veya doktor adı

def listen_tcp(sock):
    try:
        while True:
            msg = sock.recv(BUFFER_SIZE).decode()
            if not msg:
                break
            print(f"[Sunucu]: {msg}")
            if "randevu teklifi" in msg:
                cevap = input("Randevuyu kabul etmek için 'Kabul' yazınız: ")
                sock.send(cevap.encode())
    except:
        pass

def listen_udp(sock):
    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            msg = data.decode()
            print(f"[Sunucu]: {msg}")
            if "randevu teklifi" in msg:
                cevap = input("Randevuyu kabul etmek için 'Kabul' yazınız: ")
                sock.sendto(cevap.encode(), (HOST, PORT))
    except:
        pass

if user_type == "Doktor" and connection_type != "TCP":
    print("Doktorlar sadece TCP ile bağlanabilir!")
    sys.exit(1)

if connection_type == "TCP":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(user_type.encode())

    assigned_name = client_socket.recv(BUFFER_SIZE).decode()
    print(f"[Sunucu]: Atanan isminiz: {assigned_name}")

    msg = client_socket.recv(BUFFER_SIZE).decode()
    print(f"[Sunucu]: {msg}")

    threading.Thread(target=listen_tcp, args=(client_socket,), daemon=True).start()

    if user_type == "Doktor":
        while True:
            komut = input("Hasta çağırmak için 'Hasta Kabul' yazınız: ")
            if komut == "Hasta Kabul":
                client_socket.send(komut.encode())

    else:  # Hasta ise burada sonsuz bekleme yapılacak
        while True:
            time.sleep(1)

elif connection_type == "UDP":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(user_type.encode(), (HOST, PORT))

    data, addr = client_socket.recvfrom(BUFFER_SIZE)
    assigned_name = data.decode()
    print(f"[Sunucu]: Atanan isminiz: {assigned_name}")

    data, addr = client_socket.recvfrom(BUFFER_SIZE)
    print(f"[Sunucu]: {data.decode()}")

    threading.Thread(target=listen_udp, args=(client_socket,), daemon=True).start()

    while True:
        time.sleep(1)

else:
    print("Bağlantı tipi TCP veya UDP olmalıdır!")
    sys.exit(1)
