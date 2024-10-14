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
