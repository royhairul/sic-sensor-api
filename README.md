# SIC-SENSOR-API

SIC-SENSOR-API adalah sistem API untuk menghubungkan dan mengelola data dari sensor IoT, dengan integrasi ke **Ubidots** (platform IoT) dan **MongoDB** (database NoSQL). API ini memungkinkan komunikasi data sensor menggunakan **MQTT** dan **REST API**, serta menyediakan penyimpanan data lokal menggunakan MongoDB.

## 📌 Fitur Utama
- **Koneksi MQTT ke Ubidots** untuk mengirim data sensor secara real-time.
- **Integrasi REST API dengan MongoDB** untuk penyimpanan dan pengelolaan data sensor.
- **Endpoint API** untuk mengakses dan mengelola data sensor.
- **Dokumentasi proyek** untuk memudahkan penggunaan dan pengembangan lebih lanjut.

---

## 📂 Struktur Proyek
```
SIC-SENSOR-API/
│── api/
│   ├── main.py                # File utama untuk menjalankan API
│
│── code/
│   ├── connect_mqtt_ubidots.py    # Koneksi ke Ubidots menggunakan MQTT
│   ├── connect_rest_api_mongodb.py # Integrasi REST API dengan MongoDB
│
│── docs/
│   ├── dashboard-ubidots.jpg   # Dokumentasi tampilan dashboard Ubidots
│   ├── skema-integrasi.png     # Diagram/skema integrasi sistem
│
│── venv/                      # Virtual environment untuk proyek Python
│── .env.example                # Contoh konfigurasi environment variables
│── .gitignore                  # File untuk mengabaikan file tertentu dalam Git
│── requirements.txt            # Daftar dependensi yang dibutuhkan
│── setup.py                    # File setup untuk instalasi proyek
```

---

## 🚀 Instalasi
### 1️⃣ Clone Repository
```bash
git clone https://github.com/username/SIC-SENSOR-API.git
cd SIC-SENSOR-API
```

### 2️⃣ Buat Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
```

### 3️⃣ Konfigurasi Environment Variables
Buat file `.env` berdasarkan `.env.example` dan isi dengan kredensial yang diperlukan.

```env
UBIDOTS_TOKEN="your_ubidots_token"
MONGO_URI="your_mongodb_connection_string"
MQTT_BROKER="your_mqtt_broker"
```

### 4️⃣ Jalankan API
```bash
python api/main.py
```

---

## 📖 Tutorial Setup Proyek

### 📌 Persiapan Awal
1. Pastikan Python telah terinstal di komputer Anda (versi 3.8 atau lebih baru).
2. Instal **pip** dan **virtualenv** jika belum tersedia:
   ```bash
   pip install --upgrade pip
   pip install virtualenv
   ```
3. Pastikan Anda memiliki akses ke **MongoDB** dan **Ubidots API Key**.

### 🔗 Langkah-langkah Detail
#### 1️⃣ Menyiapkan Virtual Environment
- **Linux/Mac**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

#### 2️⃣ Instalasi Dependensi
```bash
pip install -r requirements.txt
```

#### 3️⃣ Konfigurasi File `.env`
- Duplikat file `.env.example` menjadi `.env`:
  ```bash
  cp .env.example .env
  ```
- Edit file `.env` dan masukkan kredensial yang diperlukan.

#### 4️⃣ Menjalankan API
```bash
python api/main.py
```

API akan berjalan pada `http://localhost:5000`, dan Anda dapat mengaksesnya melalui aplikasi klien API seperti Postman atau browser.

---
## 📡 Penggunaan API
### 🔹 Endpoint Tersedia
| Metode | Endpoint | Deskripsi |
|--------|---------|-----------|
| GET    | `/sensors` | Mengambil semua data sensor |
| POST   | `/sensors` | Menambahkan data sensor |
| GET    | `/sensors/{id}` | Mengambil data sensor berdasarkan ID |
| DELETE | `/sensors/{id}` | Menghapus data sensor |
| POST   | `/create` | Mengirim data suhu, kelembaban, dan gerakan dari sensor ESP32 |

### 🔹 Format Data JSON untuk POST `/create`
```json
{
  "temperature": 25,
  "humidity": 60,
  "motion": 1
}
```

### 🔹 Pengiriman Data melalui MQTT
- **Topik MQTT:** `samsung/`
- **Topik LED MQTT:** `samsung/led/`
- **Pesan LED:**
  - `"ON"` → Menyalakan LED
  - `"OFF"` → Mematikan LED

---
