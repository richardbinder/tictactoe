import math
import src.players as players
from src.square import Square
from src.board import Board


cache = {}


class AI:
    def __init__(self, board: Board):
        self.board_original = board
        self.board = board.deep_copy()

    def minimax(self, is_maximizing):
        if str(self.board) in cache:
            return cache[str(self.board)]

        winner = self.board.state.winner
        if winner == players.PLAYER_1:
            return 1  # AI wins
        elif winner == players.PLAYER_2:
            return -1  # Human wins
        elif self.board.state.is_draw():
            return 0  # Tie

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board.get(i, j).is_empty():
                        self.board.move(self.board.get(i, j))
                        score = self.minimax(False)
                        self.board.undo_move(self.board.get(i, j))
                        best_score = max(score, best_score)
            cache[str(self.board)] = best_score
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board.get(i, j).is_empty():
                        self.board.move(self.board.get(i, j))
                        score = self.minimax(True)
                        self.board.undo_move(self.board.get(i, j))
                        best_score = min(score, best_score)
            cache[str(self.board)] = best_score
            return best_score

    def best_move(self) -> Square:
        self.board = self.board_original.deep_copy()

        best_score = -math.inf
        position = None
        for i in range(3):
            for j in range(3):
                if self.board.get(i, j).is_empty():
                    self.board.move(self.board.get(i, j))
                    score = self.minimax(False)
                    self.board.undo_move(self.board.get(i, j))
                    if score > best_score:
                        best_score = score
                        position = self.board_original.get(i, j)
        return position
