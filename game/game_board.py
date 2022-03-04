from game.deck import Deck


class GameBoard:
    def __init__(self, players):
        self.deck = Deck()
        self.player_cards = {}

        self.give_cards(players)

        self.coins = 8
        self.lives = 3
        self.finished = False

    def play_action(self, player_id, action):
        pass

    def give_cards(self, players):
        cards_per_player = 4 if len(players) > 3 else 5

        for p in players:
            cards = [self.deck.get_card() for _ in range(cards_per_player)]

            self.player_cards[p.player_id] = cards

    def has_coins(self):
        return self.coins > 0

    def get_player_ids(self):
        return self.player_cards.keys()

    def get_player_n_cards(self, player_id):
        return len(self.player_cards.get(player_id, []))

    def get_player_colors(self, player_id):
        colors = set()
        for card in self.player_cards.get(player_id, []):
            colors.add(card.color)
        return colors

    def get_player_numbers(self, player_id):
        numbers = set()
        for card in self.player_cards.get(player_id, []):
            numbers.add(card.number)
        return numbers
