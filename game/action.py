from enum import Enum
from typing import Union
from agent.state_view import StateView
from game.hand import Hand
from game.card import CardColor


class ActionType(Enum):
    PLAY = 'PLAY'
    DISCARD = 'DISCARD'
    HINT = 'HINT'


class Action:
    """
    An action has 3 specific properties which are:
     - action_type: ActionType Enum
     - action_value: PLAYING/DISCARD the index of the card which will be discarded,
                     HINT the hint information [Color, Number]
     - effected_player_id: the player which is effected by this actions PLAYING/DISCARD the player him self,
                                                                        HINT the player which receives the hint.
    """
    def __init__(self, action_type: ActionType, action_value: Union[CardColor, int], effected_player_id: str):
        self.action_type = action_type
        self.action_value = action_value
        self.effected_player_id = effected_player_id

    def __str__(self):
        return f"Type: {self.action_type.value[0]} Value: {self.action_value} ef_player: {self.effected_player_id}"

    def short(self):
        return f"{self.action_type.value[0]} {self.action_value} {self.effected_player_id}"

    @staticmethod
    def get_player_card_actions(state_view: StateView, action_type: ActionType):
        """
        Returns all actions which can be done by a player in a specific state
        @param state_view:
        @param action_type: which action type should be considered (PLAY/DISCARD)
        @return: a list of actions
        """
        actions = []
        for index, card in enumerate(state_view.get_current_player_hand().cards):
            if card is None:
                continue
            actions.append(Action(action_type, index, state_view.get_current_player_id()))
        return actions

    @staticmethod
    def get_playing_card_actions(state_view: StateView):
        return Action.get_player_card_actions(state_view, ActionType.PLAY)

    @staticmethod
    def get_discard_card_actions(state_view: StateView):
        if state_view.coins == 8:
            return []
        return Action.get_player_card_actions(state_view, ActionType.DISCARD)

    @staticmethod
    def get_hint_actions(state_view: StateView, ignore_player_id: str):
        """
        Determines all possible hinting actions for a player in a specific state,
        with respect to ignore a specific player_id.
        @param state_view:
        @param ignore_player_id:
        @return: a list of all possible actions
        """
        actions = []
        if state_view.coins <= 0:
            return actions

        for turn, player_id in zip(range(0, len(state_view.player_ids)), state_view.player_ids):
            if player_id == ignore_player_id:
                continue
            player_hand: Hand = state_view.get_player_hand(turn)
            existing_options = player_hand.get_existing_numbers().union(player_hand.get_existing_colors())

            for option in existing_options:
                actions.append(Action(ActionType.HINT, option, player_id))
        return actions

    @staticmethod
    def get_possible_actions(state_view: StateView, ignore_player_id: str = ""):
        return Action.get_playing_card_actions(state_view) + \
               Action.get_discard_card_actions(state_view) + \
               Action.get_hint_actions(state_view, ignore_player_id)
