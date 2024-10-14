import pygame
import asyncio
import src.resources as resources
from src.entity.ai import AI
from src.render.board_render import BoardRender
from src.entity.board import Board
from src.entity.game import Game
from src.render.game_render import GameRender

pygame.init()


async def main():
    while True:
        game_restart = False

        game = Game()
        game_render = GameRender(game)
        game.set_game_render(game_render)

        while not game_restart:
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and game.board.state.has_ended:
                    game_restart = True

            game_render.update(event_list)
            game_render.draw()

            await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
