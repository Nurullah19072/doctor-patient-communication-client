# 🩺 Doktor-Hasta Randevu İstemcisi | Doctor-Patient Appointment Client

Bu proje, Python ile geliştirilmiş bir istemci uygulamasıdır ve doktor-hasta randevu sistemi simülasyonu sunar. Uygulama, kullanıcının doktor veya hasta rolünü seçmesini sağlar ve TCP veya UDP üzerinden sunucuya bağlanarak mesaj alışverişi yapılmasına olanak tanır.

---

This project is a Python-based client application that simulates a doctor-patient appointment system. It allows the user to choose a role (doctor or patient) and connect to a server using TCP or UDP to exchange messages.

---

## 📌 Özellikler | Features

- ✅ TCP veya UDP protokolü desteği  
- ✅ Kullanıcıdan rol seçimi (doktor/hasta)  
- ✅ Sunucu IP ve port bilgisiyle bağlantı  
- ✅ Terminal üzerinden mesajlaşma (örneğin randevu talebi)

- ✅ Supports TCP or UDP protocols  
- ✅ User role selection (doctor/patient)  
- ✅ Connect to server using IP and port  
- ✅ Messaging via terminal (e.g., appointment request)

---

## 💻 Gereksinimler | Requirements

- Python 3

---

## 🔧 Kullanım | Usage

### 🖥️ Sunucu Başlatma | Starting the Server

```bash
python 22100011045_Server.py
```
* TR: Sunucuyu başlatır. randevular.txt dosyasını okuyarak sistemdeki randevulu hastaları yükler. Hem TCP hem UDP bağlantılarını dinler.

* EN: Starts the server. Loads scheduled patients from randevular.txt. Listens for both TCP and UDP connections.


### Doktor (TCP)/Doctor (TCP)
```bash
python 22100011045_Client.py Doktor TCP
```
* TR: Doktor olarak TCP üzerinden bağlanır. Sunucu tarafından otomatik olarak bir isim (örn: Doktor1) atanır. Hasta çağırmak için "Hasta Kabul" yazmanız yeterlidir.

* EN: Connects as a doctor via TCP. An automatic name is assigned (e.g., Doktor1). Type "Hasta Kabul" to call the next patient.


### Hasta (TCP)/Sick (TCP)
```bash
python 22100011045_Client.py Hasta TCP
```
* TR: Hasta olarak TCP üzerinden bağlanır. Sunucu tarafından isim atanır. Doktor çağırdığında "Kabul" yazarak randevuyu onaylayabilirsiniz.

* EN: Connects as a patient via TCP. A name is assigned by the server. When a doctor calls, type "Kabul" to accept the appointment.


### Hasta (UDP)/Sick (UDP)
```bash
python 22100011045_Client.py Hasta UDP
```

* TR: Hasta olarak UDP üzerinden bağlanır. Doktor tarafından çağrıldığında "Kabul" yazarak onay verebilirsiniz.
  ⚠️ Doktorlar yalnızca TCP ile bağlanabilir.

* EN: Connects as a patient via UDP. When called by a doctor, type "Kabul" to accept the appointment.
  ⚠️ Doctors can only connect via TCP.

