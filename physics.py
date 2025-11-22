import math
import pygame

class PhysicsEngine:
    """
    Kelas statis untuk menangani perhitungan fisika yang kompleks
    seperti tumbukan antar bola.
    """
    @staticmethod
    def resolve_collision(ball1, ball2):
        # Hitung jarak vektor antara dua bola
        dx = ball1.pos.x - ball2.pos.x
        dy = ball1.pos.y - ball2.pos.y
        distance = math.hypot(dx, dy)

        # Jika jarak lebih kecil dari total jari-jari, berarti tabrakan
        if distance < ball1.radius + ball2.radius:
            # 1. Hitung Vektor Normal (arah tumbukan) dan Unit Vektornya
            # Mencegah pembagian dengan nol
            if distance == 0: distance = 0.001 
            
            nx = dx / distance
            ny = dy / distance

            # 2. Hitung Vektor Tangent (tegak lurus terhadap normal)
            tx = -ny
            ty = nx

            # 3. Proyeksikan kecepatan bola ke vektor Normal dan Tangent (Dot Product)
            # v_n = kecepatan arah tumbukan
            # v_t = kecepatan arah samping
            v1n = ball1.velocity.x * nx + ball1.velocity.y * ny
            v1t = ball1.velocity.x * tx + ball1.velocity.y * ty
            
            v2n = ball2.velocity.x * nx + ball2.velocity.y * ny
            v2t = ball2.velocity.x * tx + ball2.velocity.y * ty

            # 4. Pertukaran Momentum 1 Dimensi (Pada arah Normal saja)
            # Karena massa bola sama, kecepatan normal cukup ditukar
            v1n_final = v2n
            v2n_final = v1n

            # 5. Konversi kembali ke skalar X dan Y
            # Kecepatan baru = (Normal Baru * Vektor Normal) + (Tangent Lama * Vektor Tangent)
            ball1.velocity.x = v1n_final * nx + v1t * tx
            ball1.velocity.y = v1n_final * ny + v1t * ty
            
            ball2.velocity.x = v2n_final * nx + v2t * tx
            ball2.velocity.y = v2n_final * ny + v2t * ty

            # Mendorong bola agar tidak saling menempel (bug lengket)
            overlap = (ball1.radius + ball2.radius - distance) / 2.0
            ball1.pos.x += nx * overlap
            ball1.pos.y += ny * overlap
            ball2.pos.x -= nx * overlap
            ball2.pos.y -= ny * overlap