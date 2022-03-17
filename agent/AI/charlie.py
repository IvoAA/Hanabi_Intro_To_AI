import math
import random
import logging
from game.game_board import GameBoard
from agent.player import Player
from agent.state_view import StateView
from game.action import Action, ActionType
from tree.builder import TreeBuilder
from tree.node import SingleNode, GroupedNode
import copy

from typing import List

log = logging.getLogger(__name__)


def eval_view(game_view: StateView):
    evaluation = 0

    sure_plays = [0]*len(game_view.player_ids)
    sure_discards = [0]*len(game_view.player_ids)
    # TODO evaluate badly if important cards have been discarded (e.g. 5)
    known_playable_numbers = [0]*len(game_view.player_ids)
    known_numbers = [0]*len(game_view.player_ids)

    known_colors = [0]*len(game_view.player_ids)

    for i, hand in enumerate(game_view.get_ordered_hands()):
        for card in hand.cards:
            if not card: # TODO remove this code
                continue

            k = card.knowledge

            k_colors = k.possible_colors
            k_numbers = k.possible_numbers

            # cards the player is sure of the color
            if len(k_colors) == 1:
                known_colors[i] += 1

            # if agent has no knowledge about card, don't process it
            if len(k_numbers) == 5:
                continue

            if len(k_colors) == 1 and len(k_numbers) == 1:
                k_number = k_numbers[0]
                # if the agent knows a playable card
                if game_view.goal.get(k_colors[0]) == k_number - 1:
                    sure_plays[i] += k_number

                # the agent knows a card can be discarded
                elif game_view.goal.get(k_colors[0]) < k_number - 1:
                    sure_discards[i] += 1

                # the agent knows a card that will be needed in the future
                elif game_view.goal.get(k_colors[0]) < k_number:
                    pass

            else: # agent is not sure about card
                min_goal = 6
                max_goal = 0
                for k_color in k_colors:
                    goal_color_number = game_view.goal.get(k_color)
                    min_goal = min(min_goal, goal_color_number)
                    max_goal = max(max_goal, goal_color_number)

                # cards the player is sure of the number
                if len(k_numbers) == 1:
                    k_number = k_numbers[0]
                    # TODO check if the card will likely be needed on the future or not

                    # if all the numbers on the board are = card - 1
                    # then the player knows he can play the card
                    is_sure = True
                    for k_color in k_colors:
                        goal_color_number = game_view.goal.get(k_color)

                        if goal_color_number != k_number - 1:
                            is_sure = False

                    if is_sure:
                        sure_plays[i] += k_number
                    else:
                        known_numbers[i] += 1

                # if all cards on board are higher than max value for this card, discard
                if min(game_view.goal.values()) > max(k_numbers):
                    sure_discards[i] += 1

                # if all cards on board are lower than min value for this card, then it will be playable
                elif max(game_view.goal.values()) < min(k_numbers):
                    known_playable_numbers[i] += 1

    for i in range(len(game_view.player_ids)):
        p_eval = 0
        p_eval += 15 * sure_plays[i]
        p_eval += 5 * sure_discards[i]
        p_eval += 3 * known_playable_numbers[i]
        p_eval += 2 * known_numbers[i]
        p_eval += 1 * known_colors[i]

        # give diff importance to diff players (e.g. [1, 0.9, 0.8, ...]
        evaluation += p_eval * (1 - i*0.1)

    return evaluation


class Charlie(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)
        self.tree_builder = None

    def explore_node(self, node: SingleNode, next_player: str):
        self.game_view = StateView(node.board, next_player)

        actions = Action.get_possible_actions(self.game_view, "" if node.depth == 1 else self.player_id)
        for index, action in enumerate(actions):
            evaluation, probabilities, game_boards = self.evaluate_action(action, copy.deepcopy(self.game_board))
            if len(evaluation) == 1:
                self.tree_builder.insert_board(game_boards[0], evaluation[0], action, predecessor_node=node)
            else:
                self.tree_builder.insert_multiple_boards(game_boards, evaluation, probabilities, action, node)

    def play(self):
        log.debug(f"Turn of {self.player_id}")
        # idx starts always with zero
        self.game_view: StateView

        root_node = SingleNode(depth=0, predecessor=None, action=None, probability=1, board=self.game_board, value=0)
        root_node.is_root = True
        self.tree_builder = TreeBuilder(root_node)

        max_depth = 2

        while True:
            next_node_to_expand = self.tree_builder.get_node_to_expand()
            if next_node_to_expand.depth > 1:
                break

            if isinstance(next_node_to_expand, GroupedNode):
                nodes_to_explore = next_node_to_expand.nodes
            else:
                nodes_to_explore = [next_node_to_expand]

            if len(nodes_to_explore) > 10:
                continue

            for node in nodes_to_explore:
                current_depth = next_node_to_expand.depth
                own_idx = self.game_board.player_ids.index(self.player_id)
                next_player = self.game_board.player_ids[(own_idx + current_depth) % len(self.game_board.player_ids)]
                self.game_view = StateView(node.board, next_player)

                self.explore_node(node, next_player)

        action_to_perform = self.tree_builder.max_max()
        self.game_board.perform_action(self.player_id, action_to_perform)

    def evaluate_action(self, action: Action, game_board: GameBoard) -> (List[int], List[float], List[GameBoard]):
        lives_before = game_board.lives
        score_before = game_board.get_score()
        coins_before = game_board.coins

        new_game_boards = game_board.perform_simulated_action(self.player_id, action)
        probability_lives_after = sum(list(map(lambda r: r.get("probability") * r.get("board").lives, new_game_boards)))
        probability_score_after = sum(list(map(lambda r: r.get("probability") * r.get("board").get_score(), new_game_boards)))
        probability_coins_after = sum(list(map(lambda r: r.get("probability") * r.get("board").coins, new_game_boards)))

        lives_lost = lives_before - probability_lives_after
        diff_score = probability_score_after - score_before
        perc_coins_used = 0 if not coins_before else probability_coins_after / coins_before

        all_evaluations = []
        all_probabilities = []
        all_game_boards = []
        for board in new_game_boards:
            e = eval_view(StateView(board.get("board"), self.player_id, 1))
            if action.action_type != ActionType.DISCARD:
                e += 25
            e += 25 * perc_coins_used
            e += 100 * math.log(diff_score*10, 10) if diff_score > 0 else 0
            e *= 1 - min(0.75, lives_lost*2)

            all_evaluations.append(e)
            all_probabilities.append(board.get("probability"))
            all_game_boards.append(board.get("board"))

        return all_evaluations, all_probabilities, all_game_boards
