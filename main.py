import pygame
# --- IMPORT CLASS DARI FILE LAIN ---
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue
from physics import PhysicsEngine

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulasi Billiard - Kelompok 8")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inisialisasi Objek (Semua dimensi dikali 0.8)
        # Table: x=80, y=80, w=800, h=480
        self.table = Table(80, 80, 800, 480)
        
        # Bola Putih: x=240, y=320, radius=12 (sebelumnya 15)
        self.cue_ball = CueBall(240, 320, 12)
        
        # Setup Bola (Posisi dan radius dikali 0.8)
        self.balls = [
            self.cue_ball,
            ObjectBall(640, 320, 12, RED, 1),     # (800*0.8, 400*0.8)
            ObjectBall(668, 304, 12, YELLOW, 2),  # (835*0.8, 380*0.8)
            ObjectBall(668, 336, 12, RED, 3),     # (835*0.8, 420*0.8)
        ]
        
        self.cue = Cue(self.cue_ball)
        self.is_charging = False

    def run(self):
        while self.running:
            self._handle_events()
            self._update_logic()
            self._draw_graphics()
            self.clock.tick(FPS)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cue_ball.velocity.length() == 0:
                    self.is_charging = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if self.is_charging:
                    self.cue.shoot()
                    self.is_charging = False

    def _update_logic(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cue.update(mouse_pos)
        
        if self.is_charging:
            self.cue.power += 1
            # Batas power dikurangi jadi 40 agar sebanding dengan skala visual baru
            if self.cue.power > 40: self.cue.power = 40
            
        for ball in self.balls:
            ball.update()
            ball.check_wall_collision(self.table.rect)
            
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                PhysicsEngine.resolve_collision(self.balls[i], self.balls[j])

    def _draw_graphics(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.table.draw(self.screen)
        
        for ball in self.balls:
            ball.draw(self.screen)
            
        self.cue.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = GameManager()
    game.run()