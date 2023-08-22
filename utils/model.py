from functools import reduce
from random import choice

from static.settings import Decks
from yaml import safe_load


class Mazzo:
    def __init__(self, name=None, title=None):
        self.title = title
        words = safe_load(open(f"assets/deck/{name}.yaml")) if name else {}
        self.words = {str(word): list(map(str, taboo)) for word, taboo in words.items()}
        self.count_words = len(self.words or [])
        self.icon = name or title


class MazzoGioco:
    def __init__(self, mazzi):
        self.cards = reduce(lambda x, y: x | y.words, mazzi, {})
        self.words = list(self.cards)
        self.count_words = len(self.cards)
        icons = [{word: mazzo.icon for word in mazzo.words} for mazzo in mazzi]
        self.icons = reduce(lambda x, y: x | y, icons)
        # current
        self.current = None
        self.taboo = list()

    def next_word(self):
        if not self.words:
            return
        new_word = choice(self.words)
        new_taboo = self.cards.pop(new_word, None)
        self.words.pop(self.words.index(new_word))
        # update current
        self.current = new_word
        self.taboo = new_taboo
        self.current_icon = self.icons.get(new_word)


ALL_DECKS = [Mazzo(name, title) for name, title in Decks.options.items()]


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = MazzoGioco(ALL_DECKS)
        self.deck.next_word()
        self.score_red = 0
        self.score_blue = 0
        self.error_red = 0
        self.error_blue = 0
        self.first_team = True
        self.skip_red = 10
        self.skip_blue = 10
        self.remaining_time = 120
        self.turn_start = False
        self.turn = 1
        self.pause = False
        self.end = False


class GameSettings:
    def __init__(self):
        self.reset()

    def reset(self):
        self.decks = ALL_DECKS
        self.decks = list()
        self.duration = 120
        self.skips = 10
        self.points_to_win = 10
