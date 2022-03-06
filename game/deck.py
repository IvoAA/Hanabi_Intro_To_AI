import random

from game.card import Card, NUMBERS
from constants.card_colors import CardColor

# TODO: this should probably be somewhere else?
REPETITIONS = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1
}


class Deck:
    def __init__(self):
        self.cards = []

        for color in CardColor:
            for number in NUMBERS:
                for _ in range(REPETITIONS.get(number)):
                    self.cards.append(Card(color, number))

        self.__shuffle()

    def __shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        deck_builder = "[ "
        for card in self.cards:
            deck_builder += f"{str(card)}, "
        deck_builder = deck_builder[:-2]
        deck_builder += " ]"
        return deck_builder


