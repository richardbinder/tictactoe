import src.entity.square as square
import src.players as players
from src.entity.game_state import GameState
from src.entity.square import Square


class Board:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.turn = players.PLAYER_2
        self.state = GameState()

        self.game_array = []
        for i in range(rows):
            self.game_array.append([])
            for j in range(columns):
                self.game_array[i].append(Square(i, j))

        self.board_render = None

    def set_board_render(self, board_render):
        self.board_render = board_render

    def get_all(self) -> [Square]:
        all_squares = []
        for row in self.game_array:
            for s in row:
                all_squares.append(s)
        return all_squares

    def get_rows(self) -> [[Square]]:
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
        main_diagonal = [self.get(0, 0), self.get(1, 1), self.get(2, 2)]
        reverse_diagonal = [self.get(0, 2), self.get(1, 1), self.get(2, 0)]
        rows = self.get_rows()
        columns = self.get_columns()

        for squares in rows + columns + [main_diagonal, reverse_diagonal]:
            common = square.get_common_assignment(squares)
            if common is not None:
                return common, squares

        return None, None

    def is_board_full(self):
        return all(not self.get(i, j).is_empty() for i in range(self.rows) for j in range(self.columns))

    def deep_copy(self):
        copy = Board(self.rows, self.columns)
        copy.turn = self.turn
        copy.game_array = self.game_array
        copy.state = GameState()
        return copy

    def __str__(self):
        array_str = ""
        for s in self.get_all():
            array_str += str(s) + ","
        return array_str

