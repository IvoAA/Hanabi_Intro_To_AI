import random

from game.card import Card, COLORS, NUMBERS

# TODO: this should probably be somewhere else?
REPETITIONS = {
    "1": 3,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 1
}


class Deck:
    def __init__(self):
        self.cards = []

        for color in COLORS:
            for number in NUMBERS:
                for _ in range(REPETITIONS.get(number)):
                    self.cards.append(Card(color, number))

        self.__shuffle()

    def __shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()
