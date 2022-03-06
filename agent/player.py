from abc import ABC, abstractmethod
from game.game_board import GameBoard
from game.card import Card
from typing import Union
from constants.card_colors import CardColor


class Player(ABC):
    def __init__(self, player_id: str, game_board: GameBoard):
        self.player_id = player_id
        self.game_board = None
        self.hand = None

    @abstractmethod
    def play(self):
        pass

    def game_injection(self, game_board: GameBoard):
        self.game_board = game_board
        self.hand = self.game_board.player_hands[self.player_id]

    def play_card(self, card_idx: int) -> bool:
        result = self.game_board.card_board.play_card(self.hand.cards[card_idx])
        if not result:
            self.game_board.lives -= 1
        self.hand.cards[card_idx] = self.game_board.deck.get_card()
        return result

    # Returns false in case that there is no more coins.
    def give_hint(self, card: Card, hint: Union[CardColor, int]) -> bool:
        if self.game_board.coins > 0:
            card.give_hint(hint)
            self.game_board -= 1
            return True
        return False

    def discard_card(self, card: Card) -> bool:
        if self.game_board.coins >= 8:
            return False
        self.game_board.card_board.discard_card(card)
        return True

