import pygame
import os
import pickle
pygame.init()


# Game Settings
ROWS = 3
COLUMNS = 3
BOARD_WIDTH = 800
BOARD_HEIGHT = 800
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

# Images
IMAGE_BLUE = pygame.transform.scale(pygame.image.load("assets/images/bluecircle.png"), (150, 150))
IMAGE_GREEN = pygame.transform.scale(pygame.image.load("assets/images/greencircle.png"), (150, 150))

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
RED = (255, 0, 0)
BLUE = (70, 70, 255)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (0, 0, 100)
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
