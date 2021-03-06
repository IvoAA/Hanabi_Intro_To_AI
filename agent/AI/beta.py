import logging
import math

from agent.AI.card_counter import CardCounter
from game.card import CardKnowledge
from game.game_board import GameBoard
from agent.player import Player
from agent.state_view import StateView
from game.action import Action, ActionType
import copy

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
                    sure_plays[i] += math.ceil((6 - k_number) / 2)

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
                        sure_plays[i] += math.ceil((6 - k_number) / 2)
                    else:
                        known_numbers[i] += 1

                # if all cards on board are higher than max value for this card, discard
                if min_goal > max(k_numbers):
                    sure_discards[i] += 1

                # if all cards on board are lower than min value for this card, then it will be playable
                elif max_goal < min(k_numbers):
                    known_playable_numbers[i] += 1

    p_eval = 0
    for i in range(len(game_view.player_ids)):
        p_eval += 10 * sure_plays[i]
        p_eval += 5 * sure_discards[i]
        p_eval += 3 * known_playable_numbers[i]
        p_eval += 2 * known_numbers[i]
        p_eval += 1 * known_colors[i]

        # give diff importance to diff players (e.g. [1, 0.9, 0.8, ...]
        evaluation += p_eval * (1 - i*0.1)

    return evaluation


class Beta(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)

    def play(self):
        log.debug(f"Turn of {self.player_id}")
        self.game_view = StateView(self.game_board, self.player_id)

        self.count_cards()

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
        new_game_boards = game_board.perform_simulated_action(self.player_id, action)
        probability_lives_after = sum(list(map(lambda r: r.get("probability") * r.get("board").lives, new_game_boards)))
        probability_score_after = sum(list(map(lambda r: r.get("probability") * r.get("board").get_score(), new_game_boards)))
        probability_coins_after = sum(list(map(lambda r: r.get("probability") * r.get("board").coins, new_game_boards)))

        e = eval_view(StateView(new_game_boards[0].get("board"), self.player_id, 1))

        e += 50 * probability_coins_after
        e += 500 * probability_score_after
        e += 500 * probability_lives_after

        return e

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

