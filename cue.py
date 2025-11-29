import pygame
import math
from config import *
from physics import PhysicsEngine

class Cue:
    def __init__(self, target_ball):
        self.target_ball = target_ball
        self.angle = 0
        self.power = 0
        self.max_power = 25
        self.state = 0 
        
        self.width = 300
        self.height = 8
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (139, 69, 19), (0, 0, self.width, self.height), border_radius=4)
        pygame.draw.rect(self.image, (240, 240, 240), (0, 0, 10, self.height), border_radius=4)
        
    def update(self, mouse_pos):
        if self.state == 0:
            dx = self.target_ball.pos.x - mouse_pos[0]
            dy = self.target_ball.pos.y - mouse_pos[1]
            self.angle = math.atan2(dy, dx)
            self.power = 0
        elif self.state == 1:
            dx = self.target_ball.pos.x - mouse_pos[0]
            dy = self.target_ball.pos.y - mouse_pos[1]
            distance = math.hypot(dx, dy)
            self.power = min(max((distance - 50) / 5.0, 1), self.max_power)

    def handle_click(self):
        if self.state == 0:
            self.state = 1
            return False
        elif self.state == 1:
            self.shoot()
            self.state = 0
            return True
            
    def cancel_shot(self):
        self.state = 0
        self.power = 0

    def shoot(self):
        force = self.power
        self.target_ball.hit(force, self.angle)
        self.power = 0

    def _ray_cast_wall(self, start_pos, direction, table_rect):
        if direction.length() == 0: return start_pos
        dir_norm = direction.normalize()
        t_min = float('inf')
        
        # Cek irisan dengan setiap sisi meja
        # Pastikan tidak membagi dengan nol dan t > 0 (arah depan)
        if dir_norm.x != 0:
            if dir_norm.x < 0: # Arah Kiri
                t = (table_rect.left + BALL_RADIUS - start_pos.x) / dir_norm.x
            else: # Arah Kanan
                t = (table_rect.right - BALL_RADIUS - start_pos.x) / dir_norm.x
            if 0 < t < t_min: t_min = t
        
        if dir_norm.y != 0:
            if dir_norm.y < 0: # Arah Atas
                t = (table_rect.top + BALL_RADIUS - start_pos.y) / dir_norm.y
            else: # Arah Bawah
                t = (table_rect.bottom - BALL_RADIUS - start_pos.y) / dir_norm.y
            if 0 < t < t_min: t_min = t
            
        if t_min == float('inf'): return start_pos
        return start_pos + dir_norm * t_min

    def draw(self, surface, all_balls, table_rect):
        if self.target_ball.velocity.length() > 0 or self.target_ball.potted:
            return

        # UPDATE: Gunakan self.angle langsung agar arah garis sesuai arah tembakan (bukan terbalik)
        aim_vec = pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))
        
        # UPDATE: Filter bola agar tidak mendeteksi tabrakan dengan diri sendiri (Cue Ball)
        candidates = [b for b in all_balls if b != self.target_ball]
        hit_ball, hit_pos = PhysicsEngine.ray_cast_ball(self.target_ball.pos, aim_vec, candidates)
        
        start_pos = self.target_ball.pos
        
        # --- DRAW GUIDE LINES (HIGH CONTRAST) ---
        if hit_ball and hit_pos:
            end_pos = hit_pos
            
            # 1. GHOST BALL (Outline Putih Jelas)
            pygame.draw.circle(surface, (255, 255, 255), (int(hit_pos.x), int(hit_pos.y)), BALL_RADIUS, 2)
            
            # 2. PREDIKSI ARAH OBJEK (Solid Line)
            # Garis lurus dari ghost ball mengikuti arah tumbukan
            impact_vec = (hit_ball.pos - hit_pos).normalize()
            obj_pred_end = hit_ball.pos + impact_vec * 100
            
            # Garis Hitam (Background)
            pygame.draw.line(surface, BLACK, hit_ball.pos, obj_pred_end, 5)
            # Garis Putih (Foreground)
            pygame.draw.line(surface, WHITE, hit_ball.pos, obj_pred_end, 2)
            
            # 3. PREDIKSI ARAH CUE BALL (Solid Line)
            # Garis pantulan bola putih (tegak lurus impact)
            tangent_vec = pygame.math.Vector2(-impact_vec.y, impact_vec.x)
            # Pastikan tangent mengarah ke depan (searah dengan aim), bukan balik ke belakang
            if aim_vec.dot(tangent_vec) < 0: tangent_vec = -tangent_vec
            
            cue_pred_end = hit_pos + tangent_vec * 80
            
            pygame.draw.line(surface, BLACK, hit_pos, cue_pred_end, 4)
            pygame.draw.line(surface, (200, 200, 200), hit_pos, cue_pred_end, 2)
            
        else:
            # Jika tidak kena bola, cari dinding
            end_pos = self._ray_cast_wall(start_pos, aim_vec, table_rect)
            
        # 4. GARIS UTAMA (CUE -> TARGET/WALL)
        # Gambar garis hitam tebal dulu sebagai outline kontras
        pygame.draw.line(surface, BLACK, start_pos, end_pos, 4)
        # Gambar garis putih di atasnya
        pygame.draw.line(surface, WHITE, start_pos, end_pos, 2)

        # --- DRAW STICK ---
        angle_degrees = math.degrees(-self.angle)
        rotated_stick = pygame.transform.rotate(self.image, angle_degrees)
        pull_back = 20 + (self.power * 5)
        
        # Offset stick agar berada di belakang bola (berlawanan arah aim)
        offset_x = math.cos(self.angle) * (self.width/2 + pull_back)
        offset_y = math.sin(self.angle) * (self.width/2 + pull_back)
        
        center_x = self.target_ball.pos.x - offset_x
        center_y = self.target_ball.pos.y - offset_y
        
        rect = rotated_stick.get_rect(center=(center_x, center_y))
        surface.blit(rotated_stick, rect)