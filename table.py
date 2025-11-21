import pygame
from config import TABLE_COLOR, BORDER_COLOR

class Table:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.cushion_size = 40 

    def draw(self, surface):
        # Bingkai Kayu
        pygame.draw.rect(surface, BORDER_COLOR, 
                         (self.rect.x - self.cushion_size, 
                          self.rect.y - self.cushion_size, 
                          self.rect.width + self.cushion_size*2, 
                          self.rect.height + self.cushion_size*2))
        
        # Area Hijau
        pygame.draw.rect(surface, TABLE_COLOR, self.rect)