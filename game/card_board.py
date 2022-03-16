from constants.card_colors import CardColor
from colorama import Fore, Style
from game.card import Card


class CardBoard:
    def __init__(self):
        self.goal = {CardColor.RED: 0, CardColor.BLUE: 0, CardColor.WHITE: 0, CardColor.YELLOW: 0, CardColor.GREEN: 0}
        self.discard = []

    def discard_card(self, card: Card):
        self.discard.append(card)

    def play_card(self, card: Card) -> bool:
        if self.card_fits(card):
            self.goal[card.color] += 1
            return True
        self.discard.append(card)
        return False

    def card_fits(self, card: Card) -> bool:
        return self.goal[card.color] == card.number - 1

    def score(self):
        score = 0
        for point in self.goal.values():
            score += point
        return score

    def _goal_board_str(self) -> str:
        return f"Goal board - {Fore.RED}{self.goal[CardColor.RED]} " \
               f"{Fore.BLUE}{self.goal[CardColor.BLUE]} " \
               f"{Fore.WHITE}{self.goal[CardColor.WHITE]} " \
               f"{Fore.YELLOW}{self.goal[CardColor.YELLOW]} " \
               f"{Fore.GREEN}{self.goal[CardColor.GREEN]}" \
               f"{Style.RESET_ALL}"

    def __str__(self):
        discard_pile = f"[ {', '.join(map(str, self.discard))} ]"
        return self._goal_board_str() + f" - {discard_pile}"

    def __mini_str__(self):
        return self._goal_board_str() + f" - # discard_pile: {len(self.discard)}"

    def __to_dict__(self):
        return_dict = {
            "discard": list(map(lambda x: x.__to_dict__(), self.discard))
        }

        for key, value in self.goal.items():
            return_dict[key.value[0]] = value

        return return_dict

    @staticmethod
    def from_dict(object_dict: dict):
        new_card_board = CardBoard()
        new_card_board.goal = dict(list(map(lambda x: (x, object_dict[x.value[0]]), new_card_board.goal.keys())))
        new_card_board.discard = list(map(lambda x: Card.from_dict(x), object_dict["discard"]))
        return new_card_board
