import traceback
from game.game_board import GameBoard
from abc import ABC, abstractmethod
from typing import Union
from constants.card_colors import CardColor
from agent.state_view import StateView


class Player(ABC):
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.game_board = None
        self.hand = None
        self.game_view = None

    @abstractmethod
    def play(self):
        pass

    def game_injection(self, game_board: GameBoard):
        self.game_board = game_board
        self.hand = self.game_board.player_hands[self.player_id]
        self.game_view = StateView(game_board, self.player_id)

    def play_card(self, card_idx: int) -> bool:
        return self.game_board.play_card(self.player_id, card_idx)

    # Returns false in case that there is no more coins.
    def give_hint(self, player_id: str, hint: Union[CardColor, int]) -> bool:
        try:
            if self.game_board.coins > 0:
                target_hand = self.game_board.player_hands[player_id]
                for card in target_hand.keys():
                    card.give_hint(hint)
                self.game_board -= 1
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False

    def discard_card(self, card_idx: int) -> bool:
        self.game_board: GameBoard
        return self.game_board.discard_card(self.player_id, card_idx)

