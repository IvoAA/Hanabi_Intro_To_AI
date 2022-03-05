from game.deck import Deck
from game.hand import Hand


class GameBoard:
    def __init__(self, players):
        self.deck = Deck()
        self.player_hands = {}

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

            self.player_hands[p.player_id] = Hand(cards)

    def has_coins(self):
        return self.coins > 0

    def get_player_ids(self):
        return self.player_hands.keys()

    def get_player_n_cards(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_player_n_cards()

    def get_player_colors(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_existing_colors()

    def get_player_numbers(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_existing_numbers()
