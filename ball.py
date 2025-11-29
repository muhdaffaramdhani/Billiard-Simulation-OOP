import pygame
import math
from config import *

class Ball:
    def __init__(self, x, y, color, number=0):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = BALL_RADIUS
        self.color = color
        self.friction = 0.99
        self.potted = False
        self.number = number
        
        if number == 0: self.type = "cue"
        elif number == 8: self.type = "eight"
        elif 1 <= number <= 7: self.type = "solid"
        else: self.type = "stripe"

    def update(self):
        if self.potted: return

        self.pos += self.velocity
        if self.velocity.length() > 0.05:
            self.velocity *= self.friction
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def check_wall_collision(self, table_rect):
        if self.potted: return False
        
        collided = False
        if self.pos.x - self.radius < table_rect.left:
            self.pos.x = table_rect.left + self.radius
            self.velocity.x *= -0.9
            collided = True
        elif self.pos.x + self.radius > table_rect.right:
            self.pos.x = table_rect.right - self.radius
            self.velocity.x *= -0.9
            collided = True

        if self.pos.y - self.radius < table_rect.top:
            self.pos.y = table_rect.top + self.radius
            self.velocity.y *= -0.9
            collided = True
        elif self.pos.y + self.radius > table_rect.bottom:
            self.pos.y = table_rect.bottom - self.radius
            self.velocity.y *= -0.9
            collided = True
            
        return collided

    def check_pocket_collision(self, pockets):
        if self.potted: return False
        for pocket in pockets:
            dx = self.pos.x - pocket[0]
            dy = self.pos.y - pocket[1]
            if math.hypot(dx, dy) < POCKET_RADIUS:
                self.potted = True
                self.velocity = pygame.math.Vector2(0, 0)
                return True
        return False

    def draw(self, surface, font=None):
        if self.potted: return
        
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
        if self.type == "stripe":
            pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius - 3)
            rect_h = 10
            pygame.draw.rect(surface, self.color, (self.pos.x - self.radius + 2, self.pos.y - rect_h//2, (self.radius*2) - 4, rect_h))
        
        if self.number > 0:
            pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), 6)
            if font:
                text_surf = font.render(str(self.number), True, BLACK)
                text_rect = text_surf.get_rect(center=(int(self.pos.x), int(self.pos.y)))
                surface.blit(text_surf, text_rect)

        pygame.draw.circle(surface, (255, 255, 255), (int(self.pos.x - 3), int(self.pos.y - 3)), 2)

class CueBall(Ball):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE, 0)
        self.original_pos = (x, y)

    def reset(self):
        self.pos = pygame.math.Vector2(self.original_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.potted = False

    def hit(self, force, angle):
        impulse = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.velocity += impulse * force

class ObjectBall(Ball):
    def __init__(self, x, y, color, number):
        super().__init__(x, y, color, number)