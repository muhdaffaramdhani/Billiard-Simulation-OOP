import pygame
import math

class Cue:
    def __init__(self, target_ball):
        self.target_ball = target_ball
        self.angle = 0
        # Ukuran stik disesuaikan (300 * 0.8 = 240, 10 * 0.8 = 8)
        self.original_image = pygame.Surface((240, 8), pygame.SRCALPHA)
        self.original_image.fill((139, 69, 19)) # Coklat
        self.power = 0
        self.active = True

    def update(self, mouse_pos):
        dx = mouse_pos[0] - self.target_ball.pos.x
        dy = mouse_pos[1] - self.target_ball.pos.y
        self.angle = math.atan2(dy, dx)

    def draw(self, surface):
        # Hanya gambar stik jika bola target (putih) berhenti
        if self.active and self.target_ball.velocity.length() == 0:
            angle_degrees = math.degrees(-self.angle)
            rotated_image = pygame.transform.rotate(self.original_image, angle_degrees)
            
            # Jarak awal disesuaikan (20 * 0.8 = 16)
            distance_from_ball = 16 + self.power
            
            offset_x = math.cos(self.angle) * (self.original_image.get_width()/2 + distance_from_ball)
            offset_y = math.sin(self.angle) * (self.original_image.get_width()/2 + distance_from_ball)
            
            center_x = self.target_ball.pos.x - offset_x
            center_y = self.target_ball.pos.y - offset_y
            
            rect = rotated_image.get_rect(center=(center_x, center_y))
            surface.blit(rotated_image, rect)

    def shoot(self):
        # Batas force disesuaikan agar seimbang dengan ukuran meja baru
        # Max power di main.py sekarang 40 (sebelumnya 50)
        force = min(self.power, 40) * 0.5
        self.target_ball.hit(force, self.angle)
        self.power = 0