import src.players as players
import src.resources as resources
from src.board import Board
import pygame
import math
import warnings
from src.square import Square


class Window:
    def __init__(self, width: int, height: int, board: Board):
        self.width = width
        self.height = height
        self.board = board

        # Screen
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TicTacToe")

    def display_message(self, content):
        end_text = resources.END_FONT.render(content, 1, resources.BLACK)
        self.win.blit(end_text, ((self.width - end_text.get_width()) // 2, (self.width - end_text.get_height()) // 2))
        pygame.display.update()

    def render(self):
        self.win.fill(resources.WHITE)
        self.draw_grid(resources.BLACK, self.width // self.board.columns, self.height // self.board.rows)

        for i in range(self.board.rows):
            for j in range(self.board.columns):
                s = self.board.get(i, j)

                if not s.is_empty():
                    img = players.IMG_MAP[s.assignment]
                    self.win.blit(img, (s.x - img.get_width() // 2, s.y - img.get_height() // 2))

        if self.board.state.has_ended:
            if self.board.state.is_win():
                winning_squares = self.board.state.winning_squares
                previous_square = winning_squares[0]
                for s in winning_squares[1:]:
                    pygame.draw.line(self.win, resources.BLACK, (previous_square.x, previous_square.y), (s.x, s.y), 6)
                    previous_square = s
                self.display_message(players.CHAR_MAP[self.board.state.winner] + " has won!")
            if self.board.state.is_draw():
                self.display_message("It's a draw!")

        pygame.display.update()

    def draw_grid(self, color, gap_x, gap_y):
        for i in range(self.board.rows):
            x = i * gap_x
            pygame.draw.line(self.win, color, (x, 0), (x, self.height), 3)

        for j in range(self.board.columns):
            y = j * gap_y
            pygame.draw.line(self.win, color, (0, y), (self.width, y), 3)

    def get_mouseclick_square(self):
        m_x, m_y = pygame.mouse.get_pos()

        for i in range(self.board.rows):
            for j in range(self.board.columns):
                s = self.board.get(i, j)

                # Distance between mouse and the centre of the square
                dis_x = math.fabs(s.x-m_x)
                dis_y = math.fabs(s.y-m_y)

                max_x = self.width // self.board.rows // 2
                max_y = self.height // self.board.columns // 2

                # If it's inside the square
                if dis_x <= max_x and dis_y <= max_y and s.is_empty():
                    return s

        warnings.warn("Invalid mouse position on click")
        return None
