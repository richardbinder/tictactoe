import pygame
import src.resources as resources
from typing import Callable
from pygame.sprite import Sprite


class ButtonRender(Sprite):
    def __init__(self, parent: any, width: int, height: int, x_offset: int, y_offset: int, text: str, fnc: Callable):
        super().__init__()
        self.parent = parent
        self.fnc = fnc

        border = 20
        self.x = x_offset + border//2
        self.y = y_offset + border//2

        self.active = False

        self.image_inactive = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.image_inactive.fill(resources.LIGHT_BLUE)
        text_object_inactive = resources.BUTTON_FONT.render(text, False, resources.BLACKER)
        self.image_inactive.blit(text_object_inactive, ((width-border)//2 - text_object_inactive.get_width() // 2, (height-border)//2 - text_object_inactive.get_height() // 2))

        self.image_active = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.image_active.fill(resources.DARK_BLUE)
        text_object_active = resources.BUTTON_FONT.render(text, False, resources.WHITE)
        self.image_active.blit(text_object_active, ((width-border)//2 - text_object_active.get_width() // 2, (height-border)//2 - text_object_active.get_height() // 2))

        self.image_highlight = pygame.Surface((width-border, height-border), pygame.SRCALPHA)
        self.image_highlight.fill(resources.BLUE)
        text_object_highlight = resources.BUTTON_FONT.render(text, False, resources.BLACKER)
        self.image_highlight.blit(text_object_highlight, ((width-border)//2 - text_object_active.get_width() // 2, (height-border)//2 - text_object_active.get_height() // 2))

        self.image = self.image_inactive
        self.rect = self.image_inactive.get_rect(topleft=(self.x, self.y))

    def set_active(self):
        self.active = True
        self.image = self.image_active
        self.set_image(False)

    def set_inactive(self):
        self.active = False
        self.image = self.image_inactive
        self.set_image(False)

    def set_image(self, is_highlight: bool):
        if not self.active:
            if is_highlight:
                self.image = self.image_highlight
            else:
                self.image = self.image_inactive
        else:
            self.image = self.image_active

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos_rel = (event.pos[0] - self.parent.x, event.pos[1] - self.parent.y)
                if self.rect.collidepoint(pos_rel):
                    self.fnc()
            if event.type == pygame.MOUSEMOTION:
                pos_rel = (event.pos[0] - self.parent.x, event.pos[1] - self.parent.y)
                if self.rect.collidepoint(pos_rel):
                    self.parent.cursor = pygame.SYSTEM_CURSOR_HAND
                    self.set_image(True)
                else:
                    self.set_image(False)
