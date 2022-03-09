from game.game_board import GameBoard
import copy


class StateView:
    def __init__(self, game_board: GameBoard, player_id: str):
        self.hand = game_board.player_hands[player_id]
        self.goal = game_board.card_board.goal
        self.discarded = game_board.card_board.discard
        self.nr_players = len(game_board.player_hands)
        self.lives = game_board.lives
        self.coins = game_board.coins
        players = list(game_board.player_hands)
        self_pos = players.index(player_id)
        self.next_hand_1 = game_board.player_hands[players[(self_pos + 1) % self.nr_players]]
        self.next_hand_2 = game_board.player_hands[players[(self_pos + 2) % self.nr_players]]
        self.next_hand_3 = game_board.player_hands[players[(self_pos + 3) % self.nr_players]]

    def clone(self):
        return copy.deepcopy(self)
