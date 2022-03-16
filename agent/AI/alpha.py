import random
import logging

from agent.player import Player
from agent.state_view import StateView
from game.action import Action, ActionType

log = logging.getLogger(__name__)

class Alpha(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)

    def play(self):
        log.debug(f"Turn of {self.player_id}")
        input("Press enter to execute random task")
        self.game_view = StateView(self.game_board, self.player_id)
        # idx starts always with zero
        self.game_view: StateView
        actions = Action.get_possible_actions(self.game_view)
        action_to_perform = random.choice(actions)
        self.game_board.perform_action(self.player_id, action_to_perform)