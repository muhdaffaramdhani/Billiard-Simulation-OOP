# 🎱 Billiard  
**Simulasi Game Biliar 8-Ball Interaktif – Python & Pygame**

Billiard Master v2.5 adalah permainan biliar 8-ball yang dibangun menggunakan **Python** dan **Pygame**, dengan penerapan **OOP**, sistem fisika realistis, audio sintetis, serta antarmuka modern yang responsif.

---

## ✨ Fitur Utama

### 🎮 1. Gameplay & Fisika
- **Kontrol Stik 2-Tahap**  
  Sistem bidik (Aiming) → kunci arah → tarik mouse untuk pengisian power.
- **High Contrast Guide Lines**  
  Prediksi lintasan bola + pantulan dinding + ghost ball.
- **Fisika Realistis**  
  Termasuk friction, pantulan elastis sebagian, dan transfer momentum.
- **Aturan 8-Ball Lengkap**  
  Solid vs Stripes, foul bola putih, hingga kondisi menang/kalah saat bola 8 masuk.

---

### 🖥️ 2. Antarmuka Pengguna (UI)
- **Resolusi Widescreen 1280x800**.
- **Power Bar** visual untuk kekuatan pukulan.
- **Remaining Balls Indicator** untuk memantau bola tiap pemain.
- **Menu Lengkap**: Main Menu, Pause, Settings, Tutorial, Game Over.

---

### 🔊 3. Audio
- **Sound Generator Sintetis**  
  Suara tumbukan dan bola masuk dihasilkan secara programmatic—tanpa file `.wav` eksternal.

---

## 🚀 Cara Menjalankan

### 🔧 Prasyarat
Pastikan Python 3.x dan pygame sudah terinstal:

```bash
pip install pygame
▶️ Menjalankan Game
Jalankan dari terminal di folder proyek:

bash
Salin kode
python main.py

🕹️ Kontrol Permainan
Aksi	Input	Deskripsi
Membidik	Gerakkan Mouse	Mengarahkan stik.
Kunci Arah	Klik Kiri (1x)	Mengunci sudut bidikan dan masuk mode Power.
Atur Power	Tarik Mouse	Tarik mouse menjauhi bola untuk mengisi power.
Menembak	Klik Kiri (2x)	Melepaskan pukulan sesuai power.
Batal	Klik Kanan	Membatalkan bidikan.
Pause	Tombol MENU	Membuka menu pause.

📂 Struktur Proyek
bash
Salin kode

📁 Billiard-Master
│
├── main.py        # Entry point, game loop, UI Manager, aturan 8-ball
├── config.py      # Konfigurasi global (warna, layar, konstanta)
├── ball.py        # Class Bola (parent), CueBall, ObjectBall
├── cue.py         # Logika stik, raycasting, guide lines
├── table.py       # Rendering meja, dinding, deteksi lubang
├── physics.py     # Engine fisika (collision, friction, momentum)
└── assets/        # (opsional) jika pakai gambar tambahan

👥 Kelompok 8
Mata Kuliah: Desain Pemrograman Berorientasi Objek

📜 Lisensi
Proyek ini dapat digunakan untuk keperluan akademik, pembelajaran, atau pengembangan pribadi.