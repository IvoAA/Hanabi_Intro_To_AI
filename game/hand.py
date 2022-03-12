import game.card

from game.card import Card

class Hand:
    def __init__(self, cards):
        self.cards = []

        if len(cards) < 4 or len(cards) > 5:
            raise Exception('Wrong number of cards given when creating Hand()')

        self.cards = cards

    def get_player_n_cards(self):
        return len(self.cards)

    def get_card_by_idx(self, idx: int) -> Card:
        return self.cards[idx]

    def get_existing_colors(self):
        colors = set()
        for card in self.cards:
            colors.add(card.color)
        return colors

    def get_existing_numbers(self):
        numbers = set()
        for card in self.cards:
            numbers.add(card.number)
        return numbers

    def __str__(self):
        if self is None:
            return ""
        card_str = ', '.join(map(str, self.cards))
        knowledge_str = ', '.join(map(lambda x: str(x.knowledge) if x else 'None', self.cards))
        return f"[ {card_str} ] Knowledge: [ {knowledge_str} ]"

    def __to_list__(self):
        return list(map(lambda x: x.__to_dict__(), self.cards))

    @staticmethod
    def from_list(object_list: list):
        cards = []
        for card_object in object_list:
            cards.append(Card.from_dict(card_object))

        return Hand(cards)
