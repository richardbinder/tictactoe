import pygame
import src.players as players
import src.resources as resources
from pygame.sprite import Sprite
from src.entity.square import Square
from src.entity.game import Game


class SquareRender(Sprite):
    def __init__(self, parent: any, square: Square, width: float, height: float):
        super().__init__()
        self.square = square
        square.set_square_render(self)
        self.board_render = parent

        self.x_rel = width * square.i
        self.y_rel = height * square.j
        self.x = self.x_rel + parent.x
        self.y = self.y_rel + parent.y
        self.x_rel_center = self.x_rel + width // 2
        self.y_rel_center = self.y_rel + height // 2

        self.original_image = pygame.Surface((width-10, height-10), pygame.SRCALPHA)
        self.original_image.fill(resources.WHITE)
        self.click_image = pygame.Surface((width-10, height-10), pygame.SRCALPHA)
        self.click_image.fill(resources.WHITE)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(self.x_rel, self.y_rel))
        self.clicked = False

    def update_render(self):
        if not self.square.is_empty():
            img = players.IMG_MAP[self.square.assignment]
            self.click_image.blit(img, (self.rect.w // 2 - img.get_width() // 2, self.rect.h // 2 - img.get_height() // 2))
            self.image = self.click_image

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos_rel = (event.pos[0] - self.board_render.x, event.pos[1] - self.board_render.y)
                if self.rect.collidepoint(pos_rel):
                    self.board_render.move(self.square)

