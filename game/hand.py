class Hand:
    def __init__(self, cards):
        self.cards = {}

        if len(cards) < 4 or len(cards) > 5:
            raise Exception('Wrong number of cards given when creating Hand()')

        for i, c in enumerate(cards):
            self.cards[i] = c

    def get_player_n_cards(self):
        return len(self.cards)

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
