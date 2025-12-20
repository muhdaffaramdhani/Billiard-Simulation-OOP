import math
import pygame # type: ignore

class PhysicsEngine:
    """
    Menangani logika fisika permainan biliar, termasuk:
    1. Deteksi tumbukan antar bola (Collision Resolution).
    2. Raycasting untuk prediksi lintasan bola dan stik.
    """

    @staticmethod
    def resolve_collision(ball1, ball2):
        """
        Menyelesaikan tumbukan elastis 2D antara dua bola dengan hukum kekekalan momentum.
        Menggunakan teknik pemisahan posisi (overlap correction) untuk mencegah bola lengket.
        """
        if ball1.potted or ball2.potted:
            return False

        dx = ball1.pos.x - ball2.pos.x
        dy = ball1.pos.y - ball2.pos.y
        distance = math.hypot(dx, dy)

        if distance < ball1.radius + ball2.radius:
            if distance == 0: distance = 0.001 
            
            nx = dx / distance
            ny = dy / distance

            tx = -ny
            ty = nx

            v1n = ball1.velocity.x * nx + ball1.velocity.y * ny
            v1t = ball1.velocity.x * tx + ball1.velocity.y * ty
            
            v2n = ball2.velocity.x * nx + ball2.velocity.y * ny
            v2t = ball2.velocity.x * tx + ball2.velocity.y * ty

            v1n_final = v2n
            v2n_final = v1n

            ball1.velocity.x = v1n_final * nx + v1t * tx
            ball1.velocity.y = v1n_final * ny + v1t * ty
            
            ball2.velocity.x = v2n_final * nx + v2t * tx
            ball2.velocity.y = v2n_final * ny + v2t * ty

            overlap = (ball1.radius + ball2.radius - distance) / 2.0
            ball1.pos.x += nx * overlap
            ball1.pos.y += ny * overlap
            ball2.pos.x -= nx * overlap
            ball2.pos.y -= ny * overlap
            
            return True
        return False

    @staticmethod
    def ray_cast_ball(start_pos, direction_vector, balls):
        """
        Mendeteksi bola pertama yang akan terkena lintasan (untuk fitur aiming line).
        Mengembalikan objek bola terdekat dan titik koordinat tumbukan.
        """
        closest_dist = float('inf')
        closest_ball = None
        hit_pos = None

        if direction_vector.length() == 0: return None, None
        dir_norm = direction_vector.normalize()

        for ball in balls:
            if ball.potted: continue
            
            to_ball = ball.pos - start_pos
            proj_length = to_ball.dot(dir_norm)
            
            if proj_length < 0: continue
            
            closest_point_on_ray = start_pos + dir_norm * proj_length
            dist_to_center = closest_point_on_ray.distance_to(ball.pos)
            
            if dist_to_center < ball.radius * 2:
                dist_back = math.sqrt((ball.radius * 2)**2 - dist_to_center**2)
                impact_point = closest_point_on_ray - dir_norm * dist_back
                dist_from_start = start_pos.distance_to(impact_point)
                
                if dist_from_start < closest_dist:
                    closest_dist = dist_from_start
                    closest_ball = ball
                    hit_pos = impact_point

        return closest_ball, hit_pos