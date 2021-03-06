import copy
from typing import List

from constants.card_colors import CardColor
from game.card import Card




class CardCounter:
    @staticmethod
    def full_deck():
        cards = []
        for _ in range(3):
            for color in CardColor:
                cards.append(Card(color, 1))
        for _ in range(2):
            for color in CardColor:
                cards.append(Card(color, 2))
                cards.append(Card(color, 3))
                cards.append(Card(color, 4))
        for _ in range(1):
            for color in CardColor:
                cards.append(Card(color, 5))
        return cards

    @staticmethod
    def remaining_cards(game_board, player_id: str, root_player_id: str = '') -> List[Card]:
        remaining = CardCounter.full_deck()
        played_cards = []
        played_cards.extend(game_board.card_board.discarded_played_cards())

        played_cards.extend(game_board.card_board.goal_played_cards())

        other_players = copy.deepcopy(game_board.player_ids)
        other_players.remove(player_id)

        if root_player_id and root_player_id != player_id:
            other_players.remove(root_player_id)

        for player in other_players:
            cards = game_board.player_hands[player].cards
            played_cards.extend(cards)

        # remove Nones
        played_cards = [card for card in played_cards if card]

        for card in played_cards:
            if card in remaining:
                remaining.remove(card)

        return remaining



