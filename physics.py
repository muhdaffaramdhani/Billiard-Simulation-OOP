import math
import pygame

class PhysicsEngine:
    @staticmethod
    def resolve_collision(ball1, ball2):
        if ball1.potted or ball2.potted:
            return False

        dx = ball1.pos.x - ball2.pos.x
        dy = ball1.pos.y - ball2.pos.y
        distance = math.hypot(dx, dy)

        # Cek Tabrakan
        if distance < ball1.radius + ball2.radius:
            if distance == 0: distance = 0.001 
            
            nx = dx / distance
            ny = dy / distance
            tx, ty = -ny, nx

            v1n = ball1.velocity.x * nx + ball1.velocity.y * ny
            v1t = ball1.velocity.x * tx + ball1.velocity.y * ty
            v2n = ball2.velocity.x * nx + ball2.velocity.y * ny
            v2t = ball2.velocity.x * tx + ball2.velocity.y * ty

            # Pertukaran Momentum
            v1n_final = v2n
            v2n_final = v1n

            ball1.velocity.x = v1n_final * nx + v1t * tx
            ball1.velocity.y = v1n_final * ny + v1t * ty
            ball2.velocity.x = v2n_final * nx + v2t * tx
            ball2.velocity.y = v2n_final * ny + v2t * ty

            # Koreksi Overlap
            overlap = (ball1.radius + ball2.radius - distance) / 2.0
            ball1.pos.x += nx * overlap
            ball1.pos.y += ny * overlap
            ball2.pos.x -= nx * overlap
            ball2.pos.y -= ny * overlap
            
            return True # Terjadi tabrakan
        return False

    @staticmethod
    def ray_cast_ball(start_pos, direction_vector, balls):
        """
        Mencari bola pertama yang dipotong oleh garis (Ray Casting).
        Digunakan untuk prediksi bidikan stik.
        """
        closest_dist = float('inf')
        closest_ball = None
        hit_pos = None

        # Normalisasi arah
        if direction_vector.length() == 0: return None, None
        dir_norm = direction_vector.normalize()

        for ball in balls:
            if ball.potted: continue
            
            # Vector dari asal ray ke pusat bola
            to_ball = ball.pos - start_pos
            
            # Proyeksi titik pusat bola ke garis ray
            proj_length = to_ball.dot(dir_norm)
            
            # Jika proyeksi negatif, bola ada di belakang
            if proj_length < 0: continue
            
            closest_point_on_ray = start_pos + dir_norm * proj_length
            dist_to_center = closest_point_on_ray.distance_to(ball.pos)
            
            # Cek apakah garis menembus radius bola (dikali 2 untuk safety margin visual)
            if dist_to_center < ball.radius * 2:
                # Hitung titik tabrakan tepat di permukaan bola
                # Mundur dari pusat bola sepanjang sisa radius
                dist_back = math.sqrt((ball.radius * 2)**2 - dist_to_center**2)
                impact_point = closest_point_on_ray - dir_norm * dist_back
                
                dist_from_start = start_pos.distance_to(impact_point)
                
                if dist_from_start < closest_dist:
                    closest_dist = dist_from_start
                    closest_ball = ball
                    hit_pos = impact_point

        return closest_ball, hit_pos