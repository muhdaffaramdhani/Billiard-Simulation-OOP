import math

class PhysicsEngine:
    """
    Kelas statis untuk menangani perhitungan fisika yang kompleks
    seperti tumbukan antar bola.
    """
    @staticmethod
    def resolve_collision(ball1, ball2):
        # Hitung jarak antara dua bola
        dx = ball1.pos.x - ball2.pos.x
        dy = ball1.pos.y - ball2.pos.y
        distance = math.hypot(dx, dy)

        # Jika jarak lebih kecil dari total jari-jari, berarti tabrakan
        if distance < ball1.radius + ball2.radius:
            # Hitung sudut singgung (tangent)
            tangent = math.atan2(dy, dx)
            
            # Hitung komponen kecepatan baru (Physics Vector Math)
            angle1 = 2 * tangent - ball1.angle
            angle2 = 2 * tangent - ball2.angle
            speed1 = ball1.velocity.length()
            speed2 = ball2.velocity.length()

            # Terapkan kecepatan baru
            ball1.velocity.x = speed2 * math.cos(angle2)
            ball1.velocity.y = speed2 * math.sin(angle2)
            ball2.velocity.x = speed1 * math.cos(angle1)
            ball2.velocity.y = speed1 * math.sin(angle1)

            # --- SOLUSI TUMPANG TINDIH (OVERLAP FIX) ---
            # Memisahkan bola agar tidak lengket saat kecepatan rendah
            overlap = 0.5 * (ball1.radius + ball2.radius - distance + 1)
            ball1.pos.x += math.sin(tangent + math.pi/2) * overlap
            ball1.pos.y -= math.cos(tangent + math.pi/2) * overlap
            ball2.pos.x -= math.sin(tangent + math.pi/2) * overlap
            ball2.pos.y += math.cos(tangent + math.pi/2) * overlap