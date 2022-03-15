import random
import logging
from game.game_board import GameBoard
from agent.player import Player
from agent.state_view import StateView
from game.action import Action
import copy

log = logging.getLogger(__name__)


class Beta(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)

    def play(self):
        log.debug(f"Turn of {self.player_id}")
        self.game_view = StateView(self.game_board, self.player_id)
        # idx starts always with zero
        self.game_view: StateView
        actions = Action.get_possible_actions(self.game_view)
        idx_value = []
        for index, action in enumerate(actions):
            value = self.evaluate_board(action, copy.deepcopy(self.game_board))
            idx_value.append((index, value))

        idx_value.sort(key=lambda x: x[1], reverse=True)
        action_to_perform = actions[idx_value[0][0]]
        self.game_board.perform_action(self.player_id, action_to_perform)

    def evaluate_board(self, action: Action, game_board: GameBoard) -> int:
        lives_before = game_board.lives
        new_game_boards = game_board.perform_simulated_action(self.player_id, action)
        probability_lives_after = sum(list(map(lambda r: r.get("probability") * r.get("board").lives, new_game_boards)))
        return probability_lives_after - lives_before
