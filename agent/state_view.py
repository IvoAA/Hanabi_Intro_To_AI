# from game.game_board import GameBoard
import copy
import numpy as np


class StateView:
    def __init__(self, game_board, player_id: str, view_turn: int = 0):
        self.game_board = copy.deepcopy(game_board)
        self.player_hands = self.game_board.player_hands
        self.goal = self.game_board.card_board.goal
        self.discarded = self.game_board.card_board.discard
        self.lives = self.game_board.lives
        self.coins = self.game_board.coins
        self.player_ids = list(self.game_board.player_hands)

        self.idx_rotation = np.roll(self.player_ids, -1 * (self.player_ids.index(player_id) + view_turn))

    def clone(self):
        return copy.deepcopy(self)

    def get_current_player_id(self) -> str:
        return self.idx_rotation[0]

    def get_current_player_hand(self):
        return self.get_player_hand(0)

    def get_player_id_for_turn(self, turn_number: int) -> str:
        return self.idx_rotation[turn_number % len(self.player_ids)]

    def get_player_hand(self, turn_number: int):
        return self.player_hands[self.get_player_id_for_turn(turn_number)]

    def get_ordered_hands(self):
        hands = []

        for i in range(len(self.player_ids)):
            hands.append(self.get_player_hand(i))

        return hands
