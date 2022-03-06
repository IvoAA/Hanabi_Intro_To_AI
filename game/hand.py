import game.card

from game.card import Card

class Hand:
    def __init__(self, cards):
        self.cards = {}

        if len(cards) < 4 or len(cards) > 5:
            raise Exception('Wrong number of cards given when creating Hand()')

        for i, c in enumerate(cards):
            self.cards[i] = c

    def get_player_n_cards(self):
        return len(self.cards)

    def get_card_by_idx(self, idx: int) -> Card:
        return self.cards[idx]

    def get_existing_colors(self):
        colors = set()
        for card in self.cards.values():
            colors.add(card.color)
        return colors

    def get_existing_numbers(self):
        numbers = set()
        for card in self.cards.values():
            numbers.add(card.number)
        return numbers

    def __str__(self):
        hand_builder = "[ "
        for card in self.cards.values():
            hand_builder += f"{card}, "
        hand_builder = hand_builder[:-2]
        hand_builder += " ]"
        return hand_builder
