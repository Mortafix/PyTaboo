from functools import reduce

from static.settings import Decks
from utils.components import Button, Deck, DeckGrid, Font, Image, Text
from utils.model import Mazzo, MazzoGioco

# components
bg = Image("assets/images/origami_bg.jpeg", 100, 100)
title = Text("Seleziona i Mazzi", 50, font=Font.semibold)
btn_next = Button("confirm", 65)
btn_back = Button("back", 10)

# decks
words = {title: Mazzo(name, title) for name, title in Decks.options.items()}
mazzo_all = Mazzo()
mazzo_all.words = reduce(lambda x, y: x | y.words, words.values(), {})
mazzo_all.title = "Tutte"
mazzo_all.icon = "all"
mazzo_all.count_words = len(mazzo_all.words)
words = {"Tutte": mazzo_all} | words
decks = [Deck(deck.title, deck.icon, deck.count_words) for deck in words.values()]
deck_grid = DeckGrid(decks, 5)


def run(screen, **kwargs):
    bg.draw(screen)
    title.draw(screen, 50, 5)
    deck_grid.draw(screen)
    if [words.get(deck.title) for deck in decks if deck.selected]:
        btn_next.draw(screen, 60, 90)
    btn_back.draw(screen, 15, 90)


def manage_event(event, game, game_settings, **kwargs):
    deck_grid.handle_event(event)
    if btn_next.handle_event(event):
        if decks[0].selected:
            for deck in decks:
                deck.selected = True
        if selected_decks := [
            words.get(deck.title)
            for deck in decks
            if deck.selected and deck.title != "Tutte"
        ]:
            game_settings.decks = selected_decks
            game.deck = MazzoGioco(selected_decks)
            game.deck.next_word()
            return "game"
        return
    if btn_back.handle_event(event):
        return "custom-game"


def resize(_):
    bg.resize(100, 100)
    btn_next.resize()
    btn_back.resize()
