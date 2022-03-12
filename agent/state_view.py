from game.game_board import GameBoard
import copy
import numpy as np


class StateView:
    def __init__(self, game_board: GameBoard, player_id: str):
        self.hands = copy.deepcopy(game_board.player_hands)
        self.goal = copy.deepcopy(game_board.card_board.goal)
        self.discarded = copy.deepcopy(game_board.card_board.discard)
        self.lives = game_board.lives
        self.coins = game_board.coins
        self.player_ids = list(game_board.player_hands)
        self.idx_rotation = np.roll(self.player_ids, -1 *  self.player_ids.index(player_id))

    def clone(self):
        return copy.deepcopy(self)

    def get_current_player_hand(self):
        return self.get_player_hand(0)

    def get_player_hand(self, turn_number: int):
        turn_player_id = self.idx_rotation[turn_number % len(self.player_ids)]
        return self.hands[turn_player_id]
