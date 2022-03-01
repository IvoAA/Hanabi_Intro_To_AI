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
