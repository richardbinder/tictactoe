import pygame
import src.resources as resources
from typing import Callable
from pygame.sprite import Sprite


class ButtonRender(Sprite):
    def __init__(self, parent: any, width: int, height: int, x_offset: int, y_offset: int, text: str, color: tuple, fnc: Callable):
        super().__init__()
        self.parent = parent
        self.fnc = fnc

        border = 20
        self.x = x_offset + border//2
        self.y = y_offset + border//2

        self.image = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        text_object = resources.BUTTON_FONT.render(text, False, resources.BLACK)
        self.image.blit(text_object, ((width-border)//2 - text_object.get_width() // 2, (height-border)//2 - text_object.get_height() // 2))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos_rel = (event.pos[0] - self.parent.x, event.pos[1] - self.parent.y)
                if self.rect.collidepoint(pos_rel):
                    self.fnc()
