import math
import src.players as players
import src.resources as resources
from src.entity.square import Square
from src.entity.board import Board
from src.difficulty import Difficulty


class AI:
    def __init__(self, board: Board, difficulty: Difficulty):
        self.board_original = board
        self.board = board.deep_copy()
        self.cache = resources.ai_cache
        self.difficulty = difficulty
        self.first_move = True

    def set_difficulty(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.first_move = True

    def minimax(self, depth, is_maximizing):
        cache_key = f"{depth}, {is_maximizing}" + str(self.board)

        if cache_key in self.cache:
            return self.cache[cache_key]

        winner = self.board.state.winner
        if winner == players.PLAYER_1:
            return 1, 1, None  # AI wins
        elif winner == players.PLAYER_2:
            return -1, -1, None  # Human wins
        elif self.board.state.is_draw():
            return 0, 0, None  # Tie
        elif depth <= 0:
            return 0, 0, None

        if is_maximizing:
            best_score = -math.inf
            best_score_sum = -math.inf
            score_sum = 0
            best_pos = None
            for i in range(3):
                for j in range(3):
                    if self.board.get(i, j).is_empty():
                        self.board.move(self.board.get(i, j))
                        score, sums, _ = self.minimax(depth - 1, False)
                        self.board.undo_move(self.board.get(i, j))
                        score_sum += sums
                        if score > best_score:
                            best_score = score
                            best_score_sum = sums
                            best_pos = (i, j)
                        if score == best_score:
                            if sums >= best_score_sum:
                                best_score = score
                                best_score_sum = sums
                                best_pos = (i, j)
            self.cache[cache_key] = best_score, score_sum, best_pos
            return best_score, score_sum, best_pos
        else:
            best_score = math.inf
            best_score_sum = math.inf
            score_sum = 0
            best_pos = None
            for i in range(3):
                for j in range(3):
                    if self.board.get(i, j).is_empty():
                        self.board.move(self.board.get(i, j))
                        score, sums, _ = self.minimax(depth - 1, True)
                        self.board.undo_move(self.board.get(i, j))
                        score_sum += sums
                        if score < best_score:
                            best_score = score
                            best_score_sum = sums
                            best_pos = (i, j)
                        if score == best_score:
                            if sums <= best_score_sum:
                                best_score = score
                                best_score_sum = sums
                                best_pos = (i, j)
            self.cache[cache_key] = best_score, score_sum, best_pos
            return best_score, score_sum, best_pos

    def best_move(self) -> Square:
        return self.move_look_ahead(math.inf, True)

    def worst_move(self) -> Square:
        return self.move_look_ahead(math.inf, False)

    def move_look_ahead(self, depth, is_maximizing: bool) -> Square:
        self.board = self.board_original.deep_copy()
        _, _, best_pos = self.minimax(depth, is_maximizing)

        resources.save_ai_cache(self.cache)
        return self.board.get(best_pos[0], best_pos[1])

    def move(self):
        if self.difficulty == Difficulty.UNLOSABLE:
            return self.worst_move()
        elif self.difficulty == Difficulty.NORMAL:
            if self.first_move:
                self.first_move = False
                return self.move_look_ahead(math.inf, False)
            else:
                return self.move_look_ahead(2, True)
        elif self.difficulty == Difficulty.UNBEATABLE:
            return self.best_move()
