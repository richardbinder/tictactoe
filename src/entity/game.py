import src.resources as resources
from src.entity.ai import AI
from src.entity.board import Board


class Game:
    def __init__(self):
        self.board = Board(resources.ROWS, resources.COLUMNS)
        self.ai = AI(self.board)
        self.game_render = None

    def set_game_render(self, game_render):
        self.game_render = game_render

    def move(self, square):
        self.board.move(square)
        square.square_render.update_render()
        self.game_render.play_move_sound()
        if not self.board.state.has_ended:
            position = self.ai.best_move()
            self.board.move(position)
            position.square_render.update_render()
            self.game_render.play_move_sound()
        if self.board.state.has_ended:
            self.game_render.play_game_end_sound()
