import copy, logging

from agent.AI.card_counter import CardCounter
from constants.finish import Finish
from game.deck import Deck
from game.hand import Hand
from game.card import Card, CardColor
from game.card_board import CardBoard
from game.action import Action, ActionType
from itertools import product

log = logging.getLogger(__name__)

class GameBoard:
    def __init__(self, players):
        self.deck = Deck()
        self.player_hands = {}
        self.player_ids = list(map(lambda x: x.player_id, players))
        self.give_cards()

        self.coins = 8
        self.lives = 3
        self.finished = False
        self.turns_before_end = len(self.player_ids) + 1
        self.card_board = CardBoard()
        self.nr_actions = 0
        self.finish_reason = None

    def perform_action(self, player_id, action: Action):
        log.info(f"[PERFORM] Player: {player_id} action: {action}")
        self.nr_actions += 1
        if action.action_type == ActionType.PLAY:
            self.play_card(player_id, action.action_value)
        elif action.action_type == ActionType.DISCARD:
            self.discard_card(player_id, action.action_value)
        elif action.action_type == ActionType.HINT:
            self.hint(player_id, action)


    def perform_simulated_action(self, player_id, action: Action):
        log.debug(f"[SIMULATE] Player: {player_id} action: {action}")
        if action.action_type == ActionType.PLAY:
            return self.play_card_with_possibilities(player_id, action.action_value)
        elif action.action_type == ActionType.DISCARD:
            self.discard_card(player_id, action.action_value)
        elif action.action_type == ActionType.HINT:
            self.hint(player_id, action)
        return [{"probability": 1, "board": copy.deepcopy(self)}]

    def play_card_with_possibilities(self, player_id, card_idx: int):
        player_card: Card = self.player_hands[player_id].cards[card_idx]
        possible_colors = player_card.knowledge.possible_colors
        possible_numbers = player_card.knowledge.possible_numbers
        all_possibilities = list(product(possible_colors, possible_numbers))
        remaining_cards = CardCounter.remaining_cards(self, player_id)
        for possibility in all_possibilities:
            if not remaining_cards.__contains__(possibility):
                all_possibilities.remove(possibility)

        if len(all_possibilities) == 1:
            new_board = copy.deepcopy(self)
            new_board.play_card(player_id, card_idx)
            return [{"probability": 1, "board": new_board}]

        copied_boards = [copy.deepcopy(self) for _ in range(len(all_possibilities))]
        possible_boards = []
        for possibility, board in zip(all_possibilities, copied_boards):
            board.play_fake_card(player_id,
                                 card_idx,
                                 possibility[0],
                                 possibility[1])
            possible_boards.append({"probability": 1 / len(all_possibilities), "board": board})
        return possible_boards

    def play_fake_card(self, player_id, card_idx: int, card_color: CardColor, card_number: int):
        result = self.card_board.play_card(Card(card_color, card_number))
        if not result:
            self.lives -= 1
        self.player_hands[player_id].cards[card_idx] = self.deck.get_card()

    def play_card(self, player_id, card_idx) -> bool:
        result = self.card_board.play_card(self.player_hands[player_id].cards[card_idx])
        if not result:
            self.lives -= 1
        if not self.deck.is_empty():
            self.player_hands[player_id].cards[card_idx] = self.deck.get_card()
        else:
            self.player_hands[player_id].cards[card_idx] = None
        return result

    def discard_card(self, player_id, card_idx):
        if self.coins >= 8:
            return False
        self.card_board.discard_card(self.player_hands[player_id].cards[card_idx])
        if not self.deck.is_empty():
            self.player_hands[player_id].cards[card_idx] = self.deck.get_card()
        else:
            self.player_hands[player_id].cards[card_idx] = None
        self.coins += 1
        return True

    def hint(self, player_id, action: Action):
        for card in self.player_hands[action.effected_player_id].cards:
            if card is not None:
                card.give_hint(action.action_value)
        self.coins -= 1

    def give_cards(self):
        cards_per_player = 4 if len(self.player_ids) > 3 else 5

        for player_id in self.player_ids:
            cards = [self.deck.get_card() for _ in range(cards_per_player)]
            self.player_hands[player_id] = Hand(cards)

    def has_coins(self):
        return self.coins > 0

    def get_player_ids(self):
        return self.player_hands.keys()

    def get_player_n_cards(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_player_n_cards()

    def get_player_colors(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_existing_colors()

    def get_player_numbers(self, player_id):
        if player_id not in self.player_hands:
            raise Exception(f"Player {player_id} not found")
        return self.player_hands.get(player_id).get_existing_numbers()

    def evaluate_game_finish(self):
        if self.lives == 0:
            self.finished = True
            self.finish_reason = Finish.NO_LIVE
            return

        if self.card_board.score() == 25:
            log.info(f"Game finished congratulation!")
            self.finished = True
            self.finish_reason = Finish.MAX_POINT
            return

        if self.deck.is_empty():
            if self.turns_before_end == 0:
                self.finished = True
                self.finish_reason = Finish.EMPTY_DECK
            self.turns_before_end -= 1

    def view(self):
        log.debug("Game view")
        log.debug(f"Remaining cards in Deck (end is drawn first):")
        log.debug(f"{str(self.deck)}")
        log.debug("Hands")
        max_player_id_length = max(list(map(len, self.player_ids)))
        for player_id in self.player_ids:
            log.debug(f"\t{player_id:<{max_player_id_length}} hand: {self.player_hands[player_id]}")

        if log.level == logging.DEBUG:
            log.debug(self.card_board)
        log.info(self.card_board.__mini_str__())
        log.info(f"lives: {self.lives} \t\t coins: {self.coins} \t\t score: {self.card_board.score()}")

    def __to_dict__(self):
        return {
            "deck": self.deck.__to_list__(),
            "player_hands": dict(
                list(map(lambda x: (x, self.player_hands[x].__to_list__()), self.player_hands.keys()))),
            "coins": self.coins,
            "lives": self.lives,
            "card_board": self.card_board.__to_dict__()
        }

    @staticmethod
    def from_dict(object_dict: dict, player_classes: list):
        assert (len(player_classes) == len(object_dict["player_hands"].keys()))
        new_players = []
        for cls, player_name in zip(player_classes, object_dict["player_hands"].keys()):
            new_players.append(cls(player_name, None))

        new_game_board = GameBoard(new_players)

        new_game_board.deck = Deck.from_list(object_dict["deck"])
        new_game_board.coins = object_dict["coins"]
        new_game_board.lives = object_dict["lives"]
        new_game_board.card_board = CardBoard.from_dict(object_dict["card_board"])
        new_game_board.player_hands = dict(list(map(lambda x: (x, Hand.from_list(object_dict["player_hands"][x])),
                                                    object_dict["player_hands"].keys())))

        return new_game_board

    def get_score(self):
        return self.card_board.score()
