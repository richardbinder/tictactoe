import src.players as players


class Square:
    def __init__(self, i: float, j: float):
        self.i = i
        self.j = j
        self.assignment = players.EMPTY
        self.square_render = None

    def set_square_render(self, square_render):
        self.square_render = square_render

    def set_player_1(self):
        self.assignment = players.PLAYER_1

    def set_player_2(self):
        self.assignment = players.PLAYER_2

    def set_empty(self):
        self.assignment = players.EMPTY

    def is_empty(self):
        return self.assignment == players.EMPTY

    def __str__(self):
        return f'({self.i}, {self.j}, {self.assignment})'


def get_common_assignment(square_list: list[Square]):
    if all(s.assignment != players.EMPTY and s.assignment == square_list[0].assignment for s in square_list):
        return square_list[0].assignment
    else:
        return None
