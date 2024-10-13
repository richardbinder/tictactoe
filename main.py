import numpy
import pygame
import asyncio
from src.ai import AI
from src.window import Window
from src.board import Board
from src import resources

pygame.init()


def play_move_sound():
    resources.MOVE_SOUND.play()


def play_game_start_sound():
    resources.START_SOUND.play()


def play_game_end_sound():
    resources.END_SOUND.play()


async def main():
    while True:
        game_restart = False

        board = Board(resources.ROWS, resources.COLUMNS, resources.BOARD_WIDTH, resources.BOARD_HEIGHT)
        window = Window(resources.WINDOW_WIDTH, resources.WINDOW_HEIGHT, board)
        ai = AI(board)

        play_game_start_sound()
        while not game_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if not board.state.has_ended:
                        position = window.get_mouseclick_square()
                        if position is not None:
                            board.move(position)
                            window.render()
                            play_move_sound()
                            if not board.state.has_ended:
                                position = ai.best_move()
                                board.move(position)
                                play_move_sound()
                        if board.state.has_ended:
                            play_game_end_sound()
                            pass
                    else:
                        game_restart = True

            window.render()

            await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
