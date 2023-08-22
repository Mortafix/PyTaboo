import asyncio
import sys

import pygame
from pages import custom, decks, game, menu, new_game
from static.settings import Screen
from utils.model import Game, GameSettings

# init
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Taboo")
SCREEN = pygame.display.set_mode((Screen.width, Screen.height))

# game
STATES = {
    "menu": menu,
    "new-game": new_game,
    "custom-game": custom,
    "select-decks": decks,
    "game": game,
}
GAME = Game()
GAME_SETTINGS = GameSettings()

# ---- App


async def main():
    state = "menu"
    kwargs = {"game": GAME, "game_settings": GAME_SETTINGS}
    while True:
        clock.tick(Screen.fps)
        page = STATES.get(state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            state = page.manage_event(event, **kwargs) or state
        page.run(SCREEN, **kwargs)
        pygame.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
