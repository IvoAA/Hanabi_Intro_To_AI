from game.deck import Deck


class GameBoard:
    def __init__(self, n_players=4):
        self.deck = Deck()
        self.player_cards = [[self.deck.get_card() for _ in range(4 if n_players > 3 else 5)] for _ in range(n_players)]
        self.coins = 8
        self.lives = 3
        self.finished = False

    def play_action(self, player_id, action):
        pass
