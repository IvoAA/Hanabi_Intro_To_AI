from enum import Enum
from typing import Union
from agent.state_view import StateView


class ActionType(Enum):
    PLAY = 'PLAY'
    DISCARD = 'DISCARD'
    HINT = 'HINT'


class Action:
    def __init__(self, action_type: ActionType, action_value: Union[str, int], effected_player_id: str):
        self.action_type = action_type
        self.action_value = action_value
        self.effected_player_id = effected_player_id


    @staticmethod
    def get_playing_card_actions(state_view: StateView):
        pass

    @staticmethod
    def get_possible_actions(game_board, player_id, action_type):
        # TODO return a prettier result

        # use game_board to see how many cards we can play/discard, as I assume that in the end game each player has
        # less cards in their hand (I could be wrong)
        if action_type in [PLAY, DISCARD]:
            return game_board.get_player_n_cards(player_id)
        elif action_type == HINT:
            # use game board to see which hints (if any) can be given
            actions = {}

            for other_id in game_board.get_player_ids():
                if other_id == player_id:
                    continue

                action_set = game_board.get_player_colors(other_id).union(game_board.get_existing_numbers(other_id))

                actions[other_id] = action_set

            return actions
