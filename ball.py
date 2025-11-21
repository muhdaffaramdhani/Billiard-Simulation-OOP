import pygame
import math
from config import WHITE  # Import warna yang dibutuhkan

# --- CLASS: BALL (Parent Class) ---
class Ball:
    def __init__(self, x, y, radius, color):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.friction = 0.992
        self.angle = 0

    def update(self):
        self.pos += self.velocity
        
        # Terapkan gesekan
        if self.velocity.length() > 0.05:
            self.velocity *= self.friction
        else:
            self.velocity = pygame.math.Vector2(0, 0)

        # Update sudut gerak
        if self.velocity.length() > 0:
            self.angle = math.atan2(self.velocity.y, self.velocity.x)

    def check_wall_collision(self, table_rect):
        # Pantulan Dinding Kiri & Kanan
        if self.pos.x - self.radius < table_rect.left:
            self.pos.x = table_rect.left + self.radius
            self.velocity.x *= -1
        elif self.pos.x + self.radius > table_rect.right:
            self.pos.x = table_rect.right - self.radius
            self.velocity.x *= -1

        # Pantulan Dinding Atas & Bawah
        if self.pos.y - self.radius < table_rect.top:
            self.pos.y = table_rect.top + self.radius
            self.velocity.y *= -1
        elif self.pos.y + self.radius > table_rect.bottom:
            self.pos.y = table_rect.bottom - self.radius
            self.velocity.y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

# --- CLASS: CUE BALL (Child Class) ---
class CueBall(Ball):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius, WHITE)

    def hit(self, force, angle):
        impulse = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.velocity += impulse * force

# --- CLASS: OBJECT BALL (Child Class) ---
class ObjectBall(Ball):
    def __init__(self, x, y, radius, color, number):
        super().__init__(x, y, radius, color)
        self.number = number