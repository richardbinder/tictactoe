import pygame
pygame.init()


# Game Settings
ROWS = 3
COLUMNS = 3
BOARD_WIDTH = 800
BOARD_HEIGHT = 800
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Images
IMAGE_BLUE = pygame.transform.scale(pygame.image.load("assets/images/bluecircle.png"), (150, 150))
IMAGE_GREEN = pygame.transform.scale(pygame.image.load("assets/images/greencircle.png"), (150, 150))

# Sounds
MOVE_SOUND = pygame.mixer.Sound('assets/sounds/move.ogg')
START_SOUND = pygame.mixer.Sound('assets/sounds/start.ogg')
END_SOUND = pygame.mixer.Sound('assets/sounds/end.ogg')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
END_FONT = pygame.font.SysFont(name='arial', size=80, bold=True)
