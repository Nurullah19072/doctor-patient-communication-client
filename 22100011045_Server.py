#22100011045 - Nurullah Yıldırım

import socket
import threading
import select
import time

HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024

doctors = []
patients = []
waiting_patients = []
patient_connections = {}
udp_clients = {}
randevulu_hastalar = {}

doktor_count = 0
hasta_count = 0

lock = threading.Lock()
server_running = True

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((HOST, PORT))
tcp_server.listen()

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((HOST, PORT))

print(f"[SERVER] Sunucu başlatıldı. {HOST}:{PORT}")

def load_randevular():
    try:
        with open('randevular.txt', 'r') as file:
            for line in file:
                if '=' in line:
                    doktor, hastalar = line.strip().split('=')
                    randevulu_hastalar[doktor.strip()] = [h.strip() for h in hastalar.split(',') if h.strip()]
        print("[SERVER] Randevular yüklendi:", randevulu_hastalar)
    except FileNotFoundError:
        print("[SERVER] randevular.txt dosyası bulunamadı. Randevulu hasta yok.")

def handle_tcp_client(conn, addr):
    global doktor_count, hasta_count
    try:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            conn.close()
            return

        user_type = data.strip()

        with lock:
            if user_type == "Doktor":
                doktor_count += 1
                user_name = f"Doktor{doktor_count}"
                doctors.append((user_name, conn))
                conn.send(user_name.encode())
            elif user_type == "Hasta":
                if len(doctors) == 0:
                    conn.send("Sistemde doktor yok. Bağlantı kapatılıyor.".encode())
                    conn.close()
                    return
                hasta_count += 1
                user_name = f"Hasta{hasta_count}"
                patients.append((user_name, conn))
                waiting_patients.append(user_name)
                patient_connections[user_name] = conn
                conn.send(user_name.encode())

        print(f"[SERVER] {user_name} ({user_type}) TCP ile bağlandı: {addr}")
        conn.send("Hoşgeldiniz!".encode())

        while True:
            msg = conn.recv(BUFFER_SIZE).decode()
            if not msg:
                break
            if msg == "Hasta Kabul" and user_type == "Doktor":
                assign_next_patient(user_name, conn)
            elif user_type == "Hasta" and msg.strip() == "Kabul":
                with lock:
                    patient_connections[user_name] = "Kabul"
    except:
        pass
    finally:
        with lock:
            if (user_name, conn) in doctors:
                doctors.remove((user_name, conn))
            if (user_name, conn) in patients:
                patients.remove((user_name, conn))
            if user_name in patient_connections:
                patient_connections.pop(user_name, None)
        conn.close()

def handle_udp_client(data, addr):
    global hasta_count
    user_name = None
    try:
        user_type = data.decode().strip()

        with lock:
            if user_type == "Hasta":
                if len(doctors) == 0:
                    udp_server.sendto("Sistemde doktor yok. Bağlantı kapatılıyor.".encode(), addr)
                    return
                hasta_count += 1
                user_name = f"Hasta{hasta_count}"
                patients.append((user_name, addr))
                waiting_patients.append(user_name)
                udp_clients[user_name] = addr
                udp_server.sendto(user_name.encode(), addr)

        if user_name:
            print(f"[SERVER] {user_name} ({user_type}) UDP ile bağlandı: {addr}")
            udp_server.sendto("Hoşgeldiniz!".encode(), addr)

    except Exception as e:
        print(f"[SERVER] UDP hata: {e}")


def assign_next_patient(doctor_name, doctor_conn):
    with lock:
        next_patient = None

        # Önce kendi randevulu hastasından
        randevu_listesi = randevulu_hastalar.get(doctor_name, [])
        if randevu_listesi:
            next_patient = randevu_listesi[0]  # pop yapma, önce kontrol edelim

        # Kendi listesi boşsa diğerlerinden
        if not next_patient:
            max_doktor = None
            max_sayi = 0
            for d_adi, hastalar in randevulu_hastalar.items():
                if d_adi != doctor_name and len(hastalar) > max_sayi:
                    max_doktor = d_adi
                    max_sayi = len(hastalar)
            if max_doktor:
                next_patient = randevulu_hastalar[max_doktor][0]


        # O da yoksa bekleyenlerden
        if not next_patient and waiting_patients:
            next_patient = waiting_patients[0]

        if not next_patient:
            doctor_conn.send("Bekleyen hasta bulunmamaktadır.".encode())
            return

        # Hasta her nerede listelenmişse sil
        for d_adi in list(randevulu_hastalar):
            if next_patient in randevulu_hastalar[d_adi]:
                randevulu_hastalar[d_adi].remove(next_patient)
        if next_patient in waiting_patients:
            waiting_patients.remove(next_patient)

    # --- TCP Hasta mı?
    if next_patient in patient_connections:
        conn_or_status = patient_connections[next_patient]
        if isinstance(conn_or_status, socket.socket):
            conn = conn_or_status
            try:
                conn.send(f"{next_patient} -> {doctor_name} randevu teklifi".encode())
                doctor_conn.send(f"{next_patient} -> {doctor_name} çağrıldı.".encode())
            except:
                doctor_conn.send(f"{next_patient} ile iletişim kurulamadı.".encode())
                return

            start_time = time.time()
            responded = False
            while time.time() - start_time < 10:
                with lock:
                    if patient_connections.get(next_patient) == "Kabul":
                        doctor_conn.send(f"{next_patient} Doktor {doctor_name} randevusunu kabul etti".encode())
                        try:
                            conn.send("Geçmiş olsun.".encode())
                        except:
                            pass
                        responded = True
                        break
                time.sleep(0.5)

            if not responded:
                doctor_conn.send(f"{next_patient} yanıt vermedi.".encode())
                # Tekrar bekleyenler listesine al
                with lock:
                    waiting_patients.append(next_patient)
                    patient_connections[next_patient] = conn  # Bağlantıyı tekrar ekle
            else:
                with lock:
                    patient_connections.pop(next_patient, None)

        else:
            doctor_conn.send(f"{next_patient} ile iletişim hatası.".encode())

    # --- UDP Hasta mı?
    elif next_patient in udp_clients:
        addr = udp_clients.get(next_patient)
        try:
            udp_server.sendto(f"{next_patient} -> {doctor_name} randevu teklifi".encode(), addr)
            doctor_conn.send(f"{next_patient} -> {doctor_name} çağrıldı.".encode())

            start_time = time.time()
            udp_server.setblocking(0)
            responded = False

            while time.time() - start_time < 10:
                ready = select.select([udp_server], [], [], 1)[0]
                if ready:
                    try:
                        data, recv_addr = udp_server.recvfrom(BUFFER_SIZE)
                        msg = data.decode().strip()
                        if recv_addr == addr and msg == "Kabul":
                            udp_server.sendto(f"{next_patient} Doktor {doctor_name} randevusunu kabul etti".encode(), addr)
                            doctor_conn.send(f"{next_patient} Doktor {doctor_name} randevusunu kabul etti".encode())
                            udp_server.sendto("Geçmiş olsun.".encode(), addr)
                            responded = True
                            break
                    except BlockingIOError:
                        continue

            udp_server.setblocking(1)

            if not responded:
                doctor_conn.send(f"{next_patient} yanıt vermedi.".encode())
                # Tekrar bekleme listesine al
                with lock:
                    waiting_patients.append(next_patient)
                    udp_clients[next_patient] = addr
            else:
                with lock:
                    udp_clients.pop(next_patient, None)

        except:
            doctor_conn.send(f"{next_patient} ile iletişim hatası.".encode())

    # Tüm hastalar bittiyse doktorlara bilgi ver
    with lock:
        aktif_hasta_var = bool(waiting_patients or any(randevulu_hastalar.values()) or patient_connections or udp_clients)
    if not aktif_hasta_var:
        notify_all_doctors()



def notify_all_doctors():
    global server_running
    for doc_name, conn in doctors:
        try:
            conn.send("Tüm hastalar bitmiştir. Bağlantı kapatılıyor.".encode())
            conn.close()
        except:
            pass
    print("[SERVER] Tüm doktorlara bilgi verildi. Sunucu kapatılıyor.")
    server_running = False
    try:
        tcp_server.close()
        udp_server.close()
    except:
        pass

def start_server():
    load_randevular()
    inputs = [tcp_server, udp_server]

    while server_running:
        readable, _, _ = select.select(inputs, [], [], 1)
        if not server_running:
            break
        for sock in readable:
            if sock == tcp_server:
                try:
                    conn, addr = tcp_server.accept()
                    threading.Thread(target=handle_tcp_client, args=(conn, addr)).start()
                except:
                    pass
            elif sock == udp_server:
                try:
                    data, addr = udp_server.recvfrom(BUFFER_SIZE)
                    threading.Thread(target=handle_udp_client, args=(data, addr)).start()
                except BlockingIOError:
                    continue

if __name__ == "__main__":
    start_server()
