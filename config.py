import pygame

# --- SCREEN SETTINGS ---
# Diperbesar agar ada ruang lebih luas untuk mouse di luar meja
SCREEN_WIDTH = 1280 
SCREEN_HEIGHT = 720
FPS = 60

# --- GAME DIMENSIONS ---
PLAY_WIDTH = 800
PLAY_HEIGHT = 400
# Posisi meja tetap di tengah relatif terhadap layar baru
TABLE_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TABLE_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2 + 40 

CUSHION_SIZE = 40
BALL_RADIUS = 10
POCKET_RADIUS = 20

# --- COLORS (RGB) ---
TABLE_COLOR = (34, 139, 34)
BORDER_COLOR = (80, 40, 0)
POCKET_COLOR = (10, 10, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
DARK_GREY = (30, 30, 30)

# Bola Warna
YELLOW = (255, 215, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
MAROON = (128, 0, 0)

# UI Colors
UI_BG = (20, 25, 30)
ACCENT_COLOR = (255, 140, 0) # Orange terang
TEXT_COLOR = (240, 240, 240)
BUTTON_HOVER = (50, 50, 60)

# --- GAME STATES ---
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_TUTORIAL = "tutorial"
STATE_SETTINGS = "settings"
STATE_PAUSED = "paused" # State baru