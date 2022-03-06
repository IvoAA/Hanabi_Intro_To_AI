from colorama import Fore
from colorama import Style
from constants.card_colors import CardColor
from typing import Union


NUMBERS = [1, 2, 3, 4, 5]

class CardKnowledge:
    def __init__(self):
        self.possible_colors = list(CardColor)
        self.possible_numbers = list(NUMBERS)

    def update_colors(self, color: CardColor):
        self.possible_colors = [color]

    def update_numbers(self, number):
        self.possible_numbers = [number]


class Card:
    def __init__(self, color: CardColor, number: int):
        self.color = color
        self.number = number
        self.knowledge = CardKnowledge()

    def give_hint(self, hint: Union[CardColor, int]):
        if hint in CardColor:
            self.knowledge.update_colors(hint)
        elif hint in int:
            self.knowledge.update_numbers(hint)

    def get_hint(self) -> list:
        cards = []
        for color in self.knowledge.possible_colors:
            for number in self.knowledge.possible_numbers:
                cards.append(Card(color, int(number)))
        return cards

    def __str__(self):
        if self.color == CardColor.RED:
            return f"{Fore.RED}{str(self.number)}{Style.RESET_ALL}"
        if self.color == CardColor.BLUE:
            return f"{Fore.BLUE}{str(self.number)}{Style.RESET_ALL}"
        if self.color == CardColor.WHITE:
            return f"{Fore.WHITE}{str(self.number)}{Style.RESET_ALL}"
        if self.color == CardColor.YELLOW:
            return f"{Fore.YELLOW}{str(self.number)}{Style.RESET_ALL}"
        if self.color == CardColor.GREEN:
            return f"{Fore.GREEN}{str(self.number)}{Style.RESET_ALL}"
