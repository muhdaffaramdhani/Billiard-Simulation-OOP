# 🎱 Billiard Master Simulation

**Billiard Master** adalah simulasi permainan biliar **8-ball** berbasis desktop yang dikembangkan menggunakan **Python** dan **Pygame**. Proyek ini dirancang sebagai **Final Project** untuk mata kuliah **Desain Pemrograman Berorientasi Objek**, dengan fokus pada penerapan **OOP**, **fisika 2D realistis**, serta **manajemen data lokal**.

---

## 📑 Table of Contents
- [Pendahuluan](#-pendahuluan)
- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Struktur Proyek](#-struktur-proyek)
- [Instalasi & Menjalankan Program](#-instalasi--menjalankan-program)
- [Membuat File Executable (.exe)](#-membuat-file-executable-exe)
- [Kontrol Permainan](#-kontrol-permainan)
- [Tim Pengembang](#-tim-pengembang)
- [Lisensi](#-lisensi)

---

## 📘 Pendahuluan

Billiard Master mensimulasikan permainan biliar 8-ball dengan aturan resmi dan mekanisme permainan yang realistis. Game ini menerapkan:
- **Object-Oriented Programming (OOP)**
- **Physics Engine 2D**
- **Collision Detection & Resolution**
- **Local Leaderboard berbasis file JSON**

---

## ✨ Fitur Utama

### 🎮 Gameplay & Fisika
- **Realistic Physics Engine**  
  Simulasi tumbukan elastis, gesekan (friction), dan transfer momentum antar bola.
  
- **Precision Aiming System**  
  Dilengkapi *guide line* dan *ghost ball* untuk memprediksi arah bola.

- **Mekanisme Stik 2-Tahap**  
  - Klik pertama: mengunci arah  
  - Tarik mouse: mengatur kekuatan  
  - Klik kedua: menembak

- **Peraturan 8-Ball Resmi**
  - Foul jika bola putih masuk lubang  
  - Penentuan otomatis bola **Solid / Stripes**  
  - Kondisi menang/kalah berdasarkan bola 8  

### 🏆 Fitur Final Update
- **Local Leaderboard**  
  Menyimpan nama pemain dan jumlah kemenangan secara permanen menggunakan file JSON.
  
- **Player Name Input**  
  Pemain dapat memasukkan nama sebelum pertandingan dimulai.

- **Interactive UI**  
  Menu modern, tutorial dalam game, serta pengaturan sensitivitas mouse.

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi |
|--------|----------|
| Bahasa | Python 3.x |
| Library | Pygame |
| Audio | Synthesized Sound (tanpa file eksternal) |
| Data Storage | JSON (Leaderboard) |

---

## 📂 Struktur Proyek

Proyek ini dirancang secara modular dengan prinsip **OOP**:

```

📦 BilliardMaster
┣ 📜 main.py          # GameManager (Game Loop & State Management)
┣ 📜 physics.py       # PhysicsEngine (Collision & Vector Math)
┣ 📜 ball.py          # Ball, CueBall, ObjectBall (Inheritance)
┣ 📜 cue.py           # Cue Stick & Aiming Logic
┣ 📜 table.py         # Meja, Cushion, Area Permainan
┣ 📜 leaderboard.py   # I/O JSON Leaderboard
┣ 📜 config.py        # Konstanta Global (Warna, FPS, Resolusi)
┣ 📜 requirements.txt
┗ 📜 leaderboard.json

````

## 🚀 Instalasi & Menjalankan Program

### 1️⃣ Prasyarat
- Python **3.8 atau lebih baru**

### 2️⃣ Instalasi Dependency
Jalankan perintah berikut di terminal:

```bash
pip install -r requirements.txt
````

### 3️⃣ Menjalankan Game

```bash
python main.py
```

---

## 📦 Membuat File Executable (.exe)

Agar game dapat dijalankan tanpa Python:

### 1️⃣ Instal PyInstaller

```bash
pip install pyinstaller
```

### 2️⃣ Build Executable

```bash
pyinstaller --noconfirm --onefile --windowed --name "BilliardMaster" main.py
```

### 3️⃣ Hasil Build

* File `.exe` akan tersedia di folder:

```
dist/BilliardMaster.exe
```

Executable ini dapat dibagikan dan dijalankan di komputer lain tanpa instalasi Python.

---

## 🕹️ Kontrol Permainan

| Aksi       | Input                      |
| ---------- | -------------------------- |
| Membidik   | Gerakkan Mouse             |
| Kunci Arah | Klik Kiri (1x)             |
| Atur Power | Tarik Mouse ke Belakang    |
| Tembak     | Klik Kiri (2x)             |
| Batal      | Klik Kanan                 |
| Pause      | Tombol di Pojok Kanan Atas |

---

## 👥 Tim Pengembang (Kelompok 8)

* **Muhammad Daffa Ramdhani** (1313624025)
* **Ricky Darmawan** (1313624007)
* **Muhammad Fabio Usama** (1313624054)

---

## 📄 Lisensi

Proyek ini dibuat **khusus untuk keperluan akademik** sebagai Tugas Akhir Mata Kuliah
**Desain Pemrograman Berorientasi Objek**.

---

🎱 *Selamat bermain dan selamat belajar OOP!*
