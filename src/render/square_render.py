import pygame
from pygame.sprite import Sprite

import src.players as players
import src.resources as resources
from src.entity.square import Square


class SquareRender(Sprite):
    def __init__(self, parent: any, square: Square, width: float, height: float):
        super().__init__()
        self.square = square
        square.set_square_render(self)
        self.parent = parent

        border = 40
        self.x_rel = width * square.i + border//2
        self.y_rel = height * square.j + border//2
        self.x = self.x_rel + parent.x
        self.y = self.y_rel + parent.y
        self.x_rel_center = self.x_rel + width // 2
        self.y_rel_center = self.y_rel + height // 2

        self.original_image = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.original_image.fill(resources.WHITE)

        self.click_image = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.click_image.fill(resources.WHITE)

        self.highlight_image = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        pygame.draw.circle(self.highlight_image, resources.LIGHT_GRAY, (self.highlight_image.get_width()//2, self.highlight_image.get_height()//2), self.highlight_image.get_height() // 2)
        # self.highlight_image.fill(resources.LIGHT_GRAY)

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(self.x_rel, self.y_rel))

    def set_image(self, is_highlight):
        if self.square.is_empty():
            if is_highlight:
                self.image = self.highlight_image
            else:
                self.image = self.original_image
        else:
            self.image = self.click_image

    def update_render(self):
        if not self.square.is_empty():
            img = players.IMG_MAP[self.square.assignment]
            self.click_image.blit(img, (self.rect.w // 2 - img.get_width() // 2, self.rect.h // 2 - img.get_height() // 2))
            self.image = self.click_image

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos_rel = (event.pos[0] - self.parent.x, event.pos[1] - self.parent.y)
                if self.rect.collidepoint(pos_rel):
                    self.parent.move(self.square)
            if event.type == pygame.MOUSEMOTION:
                pos_rel = (event.pos[0] - self.parent.x, event.pos[1] - self.parent.y)
                if self.rect.collidepoint(pos_rel):
                    self.parent.parent.cursor = pygame.SYSTEM_CURSOR_HAND
                    self.set_image(True)
                else:
                    self.set_image(False)

