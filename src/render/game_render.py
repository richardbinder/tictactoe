import pygame
from pygame.event import Event
from pygame.sprite import Sprite

import src.resources as resources
from src.entity.game import Game
from src.render.board_render import BoardRender
from src.render.button_render import ButtonRender
from src.difficulty import Difficulty


class GameRender(Sprite):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game

        self.width = resources.WINDOW_WIDTH
        self.height = resources.WINDOW_HEIGHT

        self.x = 0
        self.y = 0

        # Screen
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TicTacToe")

        self.draw_surface = pygame.Surface((self.width, self.height))
        self.offset = resources.WINDOW_HEIGHT-resources.BOARD_HEIGHT
        self.board_render = BoardRender(self, game.board, resources.BOARD_WIDTH, resources.BOARD_HEIGHT, self.offset)

        button_unlosable = ButtonRender(self, resources.WINDOW_WIDTH // 3, self.offset, 0, 0, "Unlosable", resources.LIGHT_BLUE,
                                        lambda: self.change_difficulty(Difficulty.UNLOSABLE))
        button_normal = ButtonRender(self, resources.WINDOW_WIDTH // 3, self.offset, resources.WINDOW_WIDTH // 3, 0, "Normal", resources.LIGHT_BLUE,
                                        lambda: self.change_difficulty(Difficulty.NORMAL))
        button_unbeatable = ButtonRender(self, resources.WINDOW_WIDTH // 3, self.offset, 2*resources.WINDOW_WIDTH // 3, 0, "Unbeatable", resources.LIGHT_BLUE,
                                        lambda: self.change_difficulty(Difficulty.UNBEATABLE))

        self.buttons = [button_unlosable, button_normal, button_unbeatable]
        self.play_game_start_sound()

    def change_difficulty(self, difficulty: Difficulty):
        self.game.ai.set_difficulty(difficulty)
        self.game.restart()
        self.play_game_start_sound()

    def restart(self):
        self.board_render = BoardRender(self, self.game.board, resources.BOARD_WIDTH, resources.BOARD_HEIGHT, self.offset)

    def play_game_end_sound(self):
        resources.END_SOUND.play()

    def play_move_sound(self):
        resources.MOVE_SOUND.play()

    def play_game_start_sound(self):
        resources.START_SOUND.play()

    def draw(self):
        pygame.sprite.Group([self.board_render] + self.buttons).draw(self.draw_surface)
        self.win.blit(self.draw_surface, (0, 0))
        pygame.display.update()

    def move(self, square):
        self.game.move(square)

    def update(self, event_list: list[Event]):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.game.board.state.has_ended:
                self.game.restart()

        pygame.sprite.Group([self.board_render] + self.buttons).update(event_list)
