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

TR: Sunucuyu başlatır. randevular.txt dosyasını okuyarak sistemdeki randevulu hastaları yükler. Hem TCP hem UDP bağlantılarını dinler.

EN: Starts the server. Loads scheduled patients from randevular.txt. Listens for both TCP and UDP connections.
