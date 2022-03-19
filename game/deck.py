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
    """
    The Deck contains all possible cards and is giving the cards to the players.
    """
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
        return f"[ {', '.join(map(str, self.cards))} ]"

    def __to_list__(self):
        return list(map(lambda x: x.__to_dict__(), self.cards))

    @staticmethod
    def from_list(object_list: list):
        new_deck = Deck()
        new_deck.cards = list(map(lambda x: Card.from_dict(x), object_list))
        return new_deck


