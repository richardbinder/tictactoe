import pygame
from pygame.event import Event
from pygame.sprite import Sprite

import src.resources as resources
import src.players as players
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

        self.cursor = pygame.SYSTEM_CURSOR_ARROW

        # Screen
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TicTacToe")

        self.window_surface = pygame.Surface((self.width, self.height))
        self.board_surface = pygame.Surface((resources.BOARD_WIDTH+resources.BOARD_BORDER, resources.BOARD_HEIGHT+resources.BOARD_BORDER))

        self.x_board = 0
        self.y_board = self.height - self.board_surface.get_height()

        self.board_offset_x = resources.BOARD_BORDER // 2
        self.board_offset_y = resources.BOARD_BORDER // 2 # + self.window_surface.get_height() - self.board_surface.get_height()
        self.board_render = BoardRender(self, game.board, resources.BOARD_WIDTH, resources.BOARD_HEIGHT, self.board_offset_x, self.board_offset_y)

        button_area_width = resources.BUTTON_WIDTH*3
        button_offset_x = (resources.WINDOW_WIDTH - button_area_width) // 2
        button_unlosable = ButtonRender(self, button_offset_x, 0, resources.UNLOSABLE, lambda: self.change_difficulty(Difficulty.UNLOSABLE))
        button_normal = ButtonRender(self, button_offset_x + button_area_width // 3, 0, resources.NORMAL, lambda: self.change_difficulty(Difficulty.NORMAL))
        button_unbeatable = ButtonRender(self, button_offset_x + 2 * button_area_width // 3, 0, resources.UNBEATABLE, lambda: self.change_difficulty(Difficulty.UNBEATABLE))

        self.button_difficulty_map = {
            Difficulty.UNLOSABLE: button_unlosable,
            Difficulty.NORMAL: button_normal,
            Difficulty.UNBEATABLE: button_unbeatable
        }
        self.button_difficulty_map[self.game.ai.difficulty].set_active()

        self.buttons = [button_unlosable, button_normal, button_unbeatable]
        self.play_game_start_sound()

    def change_difficulty(self, difficulty: Difficulty):
        self.button_difficulty_map[self.game.ai.difficulty].set_inactive()
        self.button_difficulty_map[difficulty].set_active()
        self.game.ai.set_difficulty(difficulty)
        self.game.restart()
        self.play_game_start_sound()

    def restart(self):
        self.board_render = BoardRender(self, self.game.board, resources.BOARD_WIDTH, resources.BOARD_HEIGHT, self.board_offset_x, self.board_offset_y)

    def play_game_end_sound(self):
        resources.END_SOUND.play()

    def play_move_sound(self):
        resources.MOVE_SOUND.play()

    def play_game_start_sound(self):
        resources.START_SOUND.play()

    def draw(self):
        self.board_surface.fill(resources.WHITE)
        pygame.sprite.Group([self.board_render]).draw(self.board_surface)
        grid = resources.GRID
        self.board_surface.blit(grid, (self.board_surface.get_width() // 2 - grid.get_width() // 2, self.board_surface.get_height() // 2 - grid.get_height() // 2))

        if self.game.board.state.is_win():
            self.draw_transparent_overlay()
            self.display_message(players.CHAR_MAP[self.game.board.state.winner] + " has won!")
        if self.game.board.state.is_draw():
            self.draw_transparent_overlay()
            self.display_message("It's a draw!")

        self.window_surface.blit(self.board_surface, (0, self.height-self.board_surface.get_height()))

        pygame.sprite.Group(self.buttons).draw(self.window_surface)

        self.win.blit(self.window_surface, (0, 0))
        pygame.display.update()

    def display_message(self, content):
        end_text = resources.END_FONT.render(content, 1, resources.BLACK)
        self.board_surface.blit(end_text, ((self.width - end_text.get_width()) // 2, (self.width - end_text.get_height()) // 2))
        pygame.display.update()

    def draw_transparent_overlay(self):
        game_over_screen_fade = pygame.Surface((self.width, self.height))
        game_over_screen_fade.fill(resources.WHITE)
        game_over_screen_fade.set_alpha(resources.OVERLAY_ALPHA)
        self.board_surface.blit(game_over_screen_fade, (0, 0))

    def move(self, square):
        self.game.move(square)

    def update(self, event_list: list[Event]):
        game_restart = False
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self.cursor = pygame.SYSTEM_CURSOR_ARROW
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.game.board.state.has_ended:
                game_restart = True

        pygame.sprite.Group([self.board_render] + self.buttons).update(event_list)
        pygame.mouse.set_cursor(self.cursor)

        if game_restart:
            self.game.restart()
