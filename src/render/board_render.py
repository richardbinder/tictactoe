import numpy as np
import pygame
import math
import warnings
import src.players as players
import src.resources as resources
from pygame.sprite import Sprite
from src.entity.game import Game
from src.entity.board import Board
from src.render.square_render import SquareRender


class BoardRender(Sprite):
    def __init__(self, parent: any, board: Board, width: int, height: int, offset: int):
        super().__init__()
        self.game_render = parent

        self.width = width
        self.height = height
        self.offset = offset
        self.board = board

        self.x = 0
        self.y = offset

        square_width = self.width // self.board.columns
        square_height = self.height // self.board.rows
        self.squares = []
        for square in self.board.get_all():
            square_render = SquareRender(self, square, square_width, square_height)
            self.squares.append(square_render)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def display_message(self, content):
        end_text = resources.END_FONT.render(content, 1, resources.BLACK)
        self.image.blit(end_text, ((self.width - end_text.get_width()) // 2, (self.width - end_text.get_height()) // 2))
        pygame.display.update()

    def update_render(self):
        self.image.fill(resources.BLACK)
        pygame.sprite.Group(self.squares).draw(self.image)

        if self.board.state.has_ended:
            self.draw_game_ending_overlay()

    def draw_game_ending_overlay(self):
        if self.board.state.is_win():
            winning_squares = [s.square_render for s in self.board.state.winning_squares]
            previous_square = winning_squares[0]
            for s in winning_squares[1:]:
                pygame.draw.line(self.image, resources.BLACK, (previous_square.x_rel_center, previous_square.y_rel_center), (s.x_rel_center, s.y_rel_center), 12)
                previous_square = s
            self.draw_transparent_overlay()
            self.display_message(players.CHAR_MAP[self.board.state.winner] + " has won!")
        if self.board.state.is_draw():
            self.draw_transparent_overlay()
            self.display_message("It's a draw!")

    def draw_transparent_overlay(self):
        game_over_screen_fade = pygame.Surface((self.width, self.height))
        game_over_screen_fade.fill(resources.WHITE)
        game_over_screen_fade.set_alpha(resources.OVERLAY_ALPHA)
        self.image.blit(game_over_screen_fade, (0, 0))

    def move(self, square):
        self.game_render.move(square)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not self.board.state.has_ended:
                    pygame.sprite.Group(self.squares).update(event_list)
        self.update_render()
