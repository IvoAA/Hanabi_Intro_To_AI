from game.deck import Deck
from game.hand import Hand
from game.card_board import CardBoard

class GameBoard:
    def __init__(self, players):
        self.deck = Deck()
        self.player_hands = {}
        self.players = players
        self.give_cards(players)

        self.coins = 8
        self.lives = 3
        self.finished = False

        self.card_board = CardBoard()

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

    def is_finish(self):
        if self.lives == 0:
            self.finished = True
            return

        if self.deck.is_empty():
            for hand in self.player_hands:
                if len(hand.cards) > 0:
                    self.finished = False
                    return
            self.finished = True

    def view(self):
        print("Game view")
        print(f"Remaining cards in Deck (end is drawn first):")
        print(self.deck)
        print()
        print("Hands")
        for player in self.players:
            print(f"\t{player.player_id} hand: {self.player_hands[player.player_id]}")

        print()
        print(self.card_board)
        print(f"lives: {self.lives} \t\t coins: {self.coins} \t\t score: {self.card_board.score()}")
