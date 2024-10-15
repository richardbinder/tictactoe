import pygame
import os
import pickle
pygame.init()


# Game Settings
ROWS = 3
COLUMNS = 3

BOARD_WIDTH = 800
BOARD_HEIGHT = 800

BOARD_BORDER = 200

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1200

BUTTON_WIDTH = 266
BUTTON_HEIGHT = 200

# Images
IMAGE_BLUE = pygame.transform.scale(pygame.image.load("assets/images/bluecircle.png"), (150, 150))
IMAGE_GREEN = pygame.transform.scale(pygame.image.load("assets/images/greencircle.png"), (150, 150))
GRID = pygame.transform.scale(pygame.image.load("assets/images/grid.png"), (BOARD_WIDTH+BOARD_BORDER, BOARD_HEIGHT+BOARD_BORDER))
UNBEATABLE = pygame.transform.scale(pygame.image.load("assets/images/unbeatable.png"), (260, 110))
UNLOSABLE = pygame.transform.scale(pygame.image.load("assets/images/unlosable.png"), (230, 120))
NORMAL = pygame.transform.scale(pygame.image.load("assets/images/normal.png"), (200, 100))

# Sounds
MOVE_SOUND = pygame.mixer.Sound('assets/sounds/move.ogg')
START_SOUND = pygame.mixer.Sound('assets/sounds/start.ogg')
END_SOUND = pygame.mixer.Sound('assets/sounds/end.ogg')

# Colors
WHITE = (180, 180, 180)
LIGHT_GRAY = (150, 150, 150)
BLACKER = (30, 30, 30)
BLACK = (50, 50, 50)
GRAY = (200, 200, 200)
RED = (150, 50, 50)
BLUE = (120, 120, 255)
LIGHT_BLUE = (180, 180, 255)
DARK_BLUE = (80, 80, 220)
OVERLAY_ALPHA = 120

# Fonts
BUTTON_FONT = pygame.font.SysFont(name='arial', size=30, bold=True)
END_FONT = pygame.font.SysFont(name='arial', size=80, bold=True)

# AI Cache
if os.path.isfile("assets/behavior/ai_cache.pkl"):
    with open("assets/behavior/ai_cache.pkl", 'rb') as file:
        ai_cache = pickle.load(file)
else:
    ai_cache = {}


def save_ai_cache(cache):
    with open("assets/behavior/ai_cache.pkl", 'wb+') as file:
        pickle.dump(cache, file)
