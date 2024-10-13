import src.resources as resources


EMPTY = 0  # Empty spot on the board
PLAYER_1 = 1  # The AI
PLAYER_2 = 2  # The human player or another opponent

CHAR_MAP = {
    EMPTY: "",
    PLAYER_1: "Blue",
    PLAYER_2: "Green"
}

IMG_MAP = {
    EMPTY: None,
    PLAYER_1: resources.IMAGE_BLUE,
    PLAYER_2: resources.IMAGE_GREEN
}