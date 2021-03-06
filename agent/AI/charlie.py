import os
import logging

from agent.AI.card_counter import CardCounter
from constants.card_colors import CardColor
from game.card import CardKnowledge
from game.game_board import GameBoard
from agent.player import Player
from agent.state_view import StateView
from game.action import Action
from tree.builder import TreeBuilder
from tree.node import SingleNode, GroupedNode
import copy
from typing import List
from dotenv import load_dotenv

load_dotenv()


log = logging.getLogger(__name__)
MAXIMUM_SCORE_V = int(os.environ["MAXIMUM_SCORE_V"])

SURE_PLAY_V = int(os.environ["SURE_PLAY_VALUE"])
SURE_DISCARD_V = int(os.environ["SURE_DISCARD_VALUE"])
KNOWN_PLAYABLE_V = int(os.environ["KNOWN_PLAYABLE_VALUE"])
KNOWN_NUMBER_V = int(os.environ["KNOWN_NUMBER_VALUE"])
KNOWN_COLOR_V = int(os.environ["KNOWN_COLORS_VALUE"])

PLAYER_LOSS_V = float(os.environ["PLAYER_LOSS_V"])

LIVES_V = int(os.environ["LIVES_VALUE"])
SCORE_V = int(os.environ["SCORE_VALUE"])
COINS_V = int(os.environ["COINS_VALUE"])

def eval_view(game_view: StateView):
    if sum(game_view.goal.values()) == 25:
        return 5000

    evaluation = 0

    sure_plays = [0]*len(game_view.player_ids)
    sure_discards = [0]*len(game_view.player_ids)

    known_playable_numbers = [0]*len(game_view.player_ids)
    known_numbers = [0]*len(game_view.player_ids)

    known_colors = [0]*len(game_view.player_ids)

    maximum_score = 25
    color_max_number = {}
    for color in CardColor:
        color_max_number[color] = 5
        for number in range(game_view.goal.get(color) + 1, 6):
            count = game_view.discarded.count((color, number))

            all_discarded = False
            if number == 1:
                if count >= 3:
                    all_discarded = True
                else:
                    maximum_score -= count/4
            elif number < 5:
                if count >= 2:
                    all_discarded = True
                else:
                    maximum_score -= count/2
            elif number == 5 and count >= 1:
                all_discarded = True

            if all_discarded:
                maximum_score -= 6 - number
                color_max_number[color] = number - 1
                break

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
                    sure_plays[i] += 1

                # the agent knows a card can be discarded
                elif game_view.goal.get(k_colors[0]) <= k_number or k_number > color_max_number[k_colors[0]]:
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
                        sure_plays[i] += 1
                    else:
                        known_numbers[i] += 1

                # if all cards on board are higher than max value for this card, discard
                if min_goal >= max(k_numbers) or max(k_numbers) > min(color_max_number.values()):
                    sure_discards[i] += 1

                # if all cards on board are lower than min value for this card, then it will be playable
                elif max_goal < min(k_numbers):
                    known_playable_numbers[i] += 1

    p_eval = maximum_score * MAXIMUM_SCORE_V
    for i in range(len(game_view.player_ids)):
        p_eval += SURE_PLAY_V * sure_plays[i]
        p_eval += SURE_DISCARD_V * sure_discards[i]
        p_eval += KNOWN_PLAYABLE_V * known_playable_numbers[i]
        p_eval += KNOWN_NUMBER_V * known_numbers[i]
        p_eval += KNOWN_COLOR_V * known_colors[i]

        # give diff importance to diff players (e.g. [1, 0.9, 0.8, ...]
        evaluation += p_eval * (1 - i*PLAYER_LOSS_V)

    return evaluation


class Charlie(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)
        self.tree_builder = None

    def explore_node(self, node: SingleNode, next_player: str):
        node_view = StateView(node.board, next_player)

        actions = Action.get_possible_actions(node_view, self.player_id)
        for index, action in enumerate(actions):
            evaluation, probabilities, game_boards = Charlie.evaluate_action(next_player, action, copy.deepcopy(node.board))
            if len(evaluation) == 1:
                self.tree_builder.insert_board(game_boards[0], evaluation[0], action, predecessor_node=node)
            else:
                self.tree_builder.insert_multiple_boards(game_boards, evaluation, probabilities, action, node)

    def play(self):
        log.debug(f"Turn of {self.player_id}")

        self.count_cards()

        # idx starts always with zero
        self.game_view: StateView

        root_node = SingleNode(depth=0, predecessor=None, action=None, probability=1, board=self.game_board, value=0)
        root_node.is_root = True
        self.tree_builder = TreeBuilder(root_node)

        max_depth = 2

        while True:
            next_node_to_expand = self.tree_builder.get_node_to_expand()
            if not next_node_to_expand or next_node_to_expand.depth > max_depth - 1:
                break

            if isinstance(next_node_to_expand, GroupedNode):
                nodes_to_explore = next_node_to_expand.nodes
            else:
                nodes_to_explore = [next_node_to_expand]

            if len(nodes_to_explore) > 10:
                continue

            for node in nodes_to_explore:
                if not node:
                    continue
                current_depth = next_node_to_expand.depth
                own_idx = self.game_board.player_ids.index(self.player_id)
                next_player = self.game_board.player_ids[(own_idx + current_depth) % len(self.game_board.player_ids)]
                self.game_view = StateView(node.board, next_player)

                self.explore_node(node, next_player)

        action_to_perform = self.tree_builder.max_max()
        self.game_board.perform_action(self.player_id, action_to_perform)

    @staticmethod
    def evaluate_action(player_id, action: Action, game_board: GameBoard, root_player_id: str = '') -> (List[int], List[float], List[GameBoard]):
        new_game_boards = game_board.perform_simulated_action(player_id, action, root_player_id)

        all_evaluations = []
        all_probabilities = []
        all_game_boards = []
        for p_board in new_game_boards:
            board = p_board.get("board")
            turns_left = board.count_remaining_cards() + len(board.player_ids)

            if board.lives == 0:
                e = board.get_score()
            else:
                e = LIVES_V * board.lives
                e += SCORE_V * board.get_score()
                e += COINS_V * min(board.coins, turns_left-2*board.coins)

                if turns_left > len(board.player_ids) + 2:
                    e += eval_view(StateView(board, player_id, 1))

            all_evaluations.append(e)
            all_probabilities.append(p_board.get("probability"))
            all_game_boards.append(board)

        return all_evaluations, all_probabilities, all_game_boards

    # if by looking at the hands of the other players, the goal board, and the discarded cards
    # it's possible to deduce that a card is not of a given number/color previously thought possible
    # -> update knowledge of said card
    def count_cards(self):
        remaining_cards = CardCounter.remaining_cards(self.game_board, self.player_id)

        # from the cards the current player could possible have, which colors would be possible for each number
        remaining_colors = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }

        for card in remaining_cards:
            if card.color not in remaining_colors[card.number]:
                remaining_colors[card.number].append(card.color)

        for card in self.game_board.player_hands[self.player_id].cards:
            if not card:
                continue

            card_knowledge: CardKnowledge = card.knowledge

            color_not_possible = {}
            for color in card_knowledge.possible_colors:
                color_not_possible[color] = True

            for number in card_knowledge.possible_numbers:

                # no remaining cards
                number_not_possible = True
                for color in card_knowledge.possible_colors:
                    if color in remaining_colors[number]:
                        number_not_possible = False
                        color_not_possible[color] = False

                if number_not_possible:
                    card_knowledge.update_numbers(number, False)

            for color in color_not_possible:
                if color_not_possible[color]:
                    card_knowledge.update_numbers(color, False)
