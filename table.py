import pygame
from config import *

class Table:
    def __init__(self):
        self.x = TABLE_X
        self.y = TABLE_Y
        self.width = PLAY_WIDTH
        self.height = PLAY_HEIGHT
        self.cushion = CUSHION_SIZE
        
        # Rect untuk area bermain (tempat bola bergerak)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Definisi posisi 6 lubang (Kiri-Atas, Tengah-Atas, Kanan-Atas, dst)
        self.pockets = [
            (self.x, self.y),                                   # Top Left
            (self.x + self.width // 2, self.y - 5),             # Top Middle (sedikit offset)
            (self.x + self.width, self.y),                      # Top Right
            (self.x, self.y + self.height),                     # Bottom Left
            (self.x + self.width // 2, self.y + self.height + 5), # Bottom Middle
            (self.x + self.width, self.y + self.height)         # Bottom Right
        ]

    def draw(self, surface):
        # 1. Gambar Bingkai Kayu (Border)
        border_rect = (
            self.x - self.cushion,
            self.y - self.cushion,
            self.width + self.cushion * 2,
            self.height + self.cushion * 2
        )
        pygame.draw.rect(surface, BORDER_COLOR, border_rect, border_radius=15)

        # 2. Gambar Area Bermain (Hijau)
        pygame.draw.rect(surface, TABLE_COLOR, self.rect)

        # 3. Gambar Lubang (Pockets)
        for pocket in self.pockets:
            pygame.draw.circle(surface, POCKET_COLOR, pocket, POCKET_RADIUS)