import numpy as np
import src.players as players
import src.square as square
from src.square import Square


class GameState:
    def __init__(self):
        self.has_ended = False
        self.winner = None
        self.winning_squares = None

    def set_win(self, winner, winning_squares):
        self.has_ended = True
        self.winner = winner
        self.winning_squares = winning_squares

    def set_draw(self):
        self.has_ended = True

    def set_undecided(self):
        self.has_ended = False
        self.winner = None
        self.winning_squares = None

    def is_win(self):
        return self.has_ended and self.winner is not None

    def is_draw(self):
        return self.has_ended and self.winner is None


class Board:
    def __init__(self, rows: int, columns: int, width: int, height: int):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.turn = players.PLAYER_2
        self.state = GameState()

        dis_to_cen_x = width // columns // 2
        dis_to_cen_y = height // rows // 2

        self.game_array = np.zeros([rows, columns], dtype=Square)
        for i in range(rows):
            for j in range(columns):
                x = dis_to_cen_x * (2 * j + 1)
                y = dis_to_cen_y * (2 * i + 1)

                self.game_array[i, j] = Square(x, y)

    def get_rows(self) -> list[list[Square]]:
        return self.game_array

    def get_columns(self) -> list[list[Square]]:
        return [self.get_c(j) for j in range(self.columns)]

    def get_r(self, i) -> list[Square]:
        return self.game_array[i]

    def get_c(self, j) -> list[Square]:
        return [self.game_array[0][j], self.game_array[1][j], self.game_array[2][j]]

    def get(self, i, j) -> Square:
        return self.game_array[i][j]

    def switch_turn(self):
        if self.turn == players.PLAYER_1:
            self.turn = players.PLAYER_2
        elif self.turn == players.PLAYER_2:
            self.turn = players.PLAYER_1

    def move(self, s: Square):
        if self.turn == players.PLAYER_1:
            s.set_player_1()
        elif self.turn == players.PLAYER_2:
            s.set_player_2()
        self.switch_turn()
        self.update_game_state()

    def undo_move(self, s: Square):
        s.set_empty()
        self.switch_turn()
        self.update_game_state()

    def update_game_state(self):
        winner, winning_squares = self.get_winner()
        if winner is not None:
            self.state.set_win(winner, winning_squares)
        elif winner is None and self.is_board_full():
            self.state.set_draw()
        else:
            self.state.set_undecided()

    def get_winner(self) -> (int, list[Square]):
        main_diagonal = np.array([self.get(0, 0), self.get(1, 1), self.get(2, 2)])
        reverse_diagonal = np.array([self.get(0, 2), self.get(1, 1), self.get(2, 0)])
        rows = self.get_rows()
        columns = self.get_columns()

        for squares in np.vstack((rows, columns, main_diagonal, reverse_diagonal)):
            common = square.get_common_assignment(squares)
            if common is not None:
                return common, squares

        return None, None

    def is_board_full(self):
        return all(not self.get(i, j).is_empty() for i in range(self.rows) for j in range(self.columns))

    def deep_copy(self):
        copy = Board(self.rows, self.columns, self.width, self.height)
        copy.turn = self.turn
        copy.game_array = self.game_array
        copy.state = GameState()
        return copy

    def __str__(self):
        return np.array2string(self.game_array, formatter={'all': lambda x: str(x)})

