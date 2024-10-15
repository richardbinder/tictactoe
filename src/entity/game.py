import src.resources as resources
from src.entity.ai import AI
from src.entity.board import Board
from src.difficulty import Difficulty


class Game:
    def __init__(self):
        self.board = Board(resources.ROWS, resources.COLUMNS)
        self.ai = AI(self.board, Difficulty.UNLOSABLE)
        self.game_render = None

    def set_game_render(self, game_render):
        self.game_render = game_render

    def restart(self):
        self.board = Board(resources.ROWS, resources.COLUMNS)
        self.ai = AI(self.board, self.ai.difficulty)
        self.game_render.restart()

    def move(self, square):
        if square.is_empty():
            self.board.move(square)
            square.square_render.update_render()
            self.game_render.play_move_sound()
            if not self.board.state.has_ended:
                position = self.ai.move()
                self.board.move(position)
                position.square_render.update_render()
                self.game_render.play_move_sound()
            if self.board.state.has_ended:
                self.game_render.play_game_end_sound()
