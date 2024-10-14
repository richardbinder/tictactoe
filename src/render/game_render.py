import pygame
from pygame.event import Event
from pygame.sprite import Sprite

import src.resources as resources
from src.entity.game import Game
from src.render.board_render import BoardRender


class GameRender(Sprite):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game

        self.width = resources.WINDOW_WIDTH
        self.height = resources.WINDOW_HEIGHT

        # Screen
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TicTacToe")

        self.draw_surface = pygame.Surface((self.width, self.height))
        self.board_render = BoardRender(self, game.board, resources.BOARD_WIDTH, resources.BOARD_HEIGHT, resources.WINDOW_HEIGHT-resources.BOARD_HEIGHT)
        self.play_game_start_sound()

    def play_game_end_sound(self):
        resources.END_SOUND.play()

    def play_move_sound(self):
        resources.MOVE_SOUND.play()

    def play_game_start_sound(self):
        resources.START_SOUND.play()

    def draw(self):
        pygame.sprite.Group([self.board_render]).draw(self.draw_surface)
        self.win.blit(self.draw_surface, (0, 0))
        pygame.display.update()

    def move(self, square):
        self.game.move(square)

    def update(self, event_list: list[Event]):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()

        self.board_render.update(event_list)
