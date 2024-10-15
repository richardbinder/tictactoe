import pygame
from pygame.sprite import Sprite

import src.players as players
import src.resources as resources
from src.entity.board import Board
from src.render.square_render import SquareRender


class BoardRender(Sprite):
    def __init__(self, parent: any, board: Board, width: int, height: int, offset_x: int, offset_y: int):
        super().__init__()
        self.parent = parent

        self.width = width
        self.height = height
        self.board = board

        self.x_rel = offset_x
        self.y_rel = offset_y
        self.x = self.x_rel + self.parent.x_board
        self.y = self.y_rel + self.parent.y_board

        square_width = self.width // self.board.columns
        square_height = self.height // self.board.rows
        self.squares = []
        for square in self.board.get_all():
            square_render = SquareRender(self, square, square_width, square_height)
            self.squares.append(square_render)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x_rel, self.y_rel))

    def update_render(self):
        self.image.fill(resources.WHITE)
        pygame.sprite.Group(self.squares).draw(self.image)

        if self.board.state.has_ended:
            self.draw_game_ending_overlay()

    def draw_game_ending_overlay(self):
        if self.board.state.is_win():
            winning_squares = [s.square_render for s in self.board.state.winning_squares]
            previous_square = winning_squares[0]
            for s in winning_squares[1:]:
                pygame.draw.line(self.image, resources.RED, (previous_square.x_rel_center, previous_square.y_rel_center), (s.x_rel_center, s.y_rel_center), 12)
                previous_square = s

    def move(self, square):
        self.parent.move(square)

    def update(self, event_list):
        if not self.board.state.has_ended:
            pygame.sprite.Group(self.squares).update(event_list)
        self.update_render()
