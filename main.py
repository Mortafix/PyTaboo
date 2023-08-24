import asyncio
import sys

import pygame
from pages import custom, decks, game, menu, new_game, rules
from static.settings import Screen
from utils.model import Game, GameSettings

# init
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Taboo")

# game
STATES = {
    "menu": menu,
    "rules": rules,
    "new-game": new_game,
    "custom-game": custom,
    "select-decks": decks,
    "game": game,
}
GAME = Game()
GAME_SETTINGS = GameSettings()

# ---- App


async def main():
    screen = pygame.display.set_mode(Screen.size)
    state = "menu"
    kwargs = {"game": GAME, "game_settings": GAME_SETTINGS}
    while True:
        clock.tick(Screen.fps)
        page = STATES.get(state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height))
                page.resize(screen)
            state = page.manage_event(event, **kwargs) or state
        page.run(screen, **kwargs)
        pygame.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
