import pygame
from config import *

class Table:
    def __init__(self):
        self.x = TABLE_X
        self.y = TABLE_Y
        self.width = PLAY_WIDTH
        self.height = PLAY_HEIGHT
        self.cushion = CUSHION_SIZE
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.pockets = [
            (self.x, self.y),
            (self.x + self.width // 2, self.y - 5),
            (self.x + self.width, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + 5),
            (self.x + self.width, self.y + self.height)
        ]

    def draw(self, surface):
        border_rect = (
            self.x - self.cushion,
            self.y - self.cushion,
            self.width + self.cushion * 2,
            self.height + self.cushion * 2
        )
        pygame.draw.rect(surface, BORDER_COLOR, border_rect, border_radius=15)
        pygame.draw.rect(surface, TABLE_COLOR, self.rect)

        for pocket in self.pockets:
            pygame.draw.circle(surface, POCKET_COLOR, pocket, POCKET_RADIUS)