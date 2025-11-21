Simulasi Permainan Billiard 2D (Python & Pygame)

Proyek ini adalah simulasi permainan billiard sederhana yang dibangun menggunakan Python dan library Pygame. Proyek ini menerapkan konsep Pemrograman Berorientasi Objek (OOP) secara modular.

👥 Anggota Kelompok 8

Muhammad Daffa Ramdhani (1313624025)
Ricky Darmawan (1313624007)
Muhammad Fabio Usama (1313624054)

📋 Fitur Minggu Ke-3
1. Struktur OOP Modular (Ball, Table, Cue dipisah).
2. Fisika dasar (Pantulan dinding & Gesekan/Friction).
3. Interaksi Stik Billiard (Rotasi mengikuti mouse & Power charging).
4. Deteksi tumbukan antar bola (Elastic Collision).

🚀 Cara Menjalankan
Prasyarat: Pastikan Python dan Pygame sudah terinstall.

pip install pygame

Jalankan Game:
Buka terminal di folder proyek, lalu jalankan:

python main.py


📂 Struktur File
main.py: Entry point program (Game Loop utama).
config.py: Konfigurasi global (Warna, Ukuran Layar, FPS).
ball.py: Class untuk logika bola (Parent & Child classes).
table.py: Class untuk rendering meja.
cue.py: Class untuk stik billiard.
physics.py: Modul logika matematika tumbukan.