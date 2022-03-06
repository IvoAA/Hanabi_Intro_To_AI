from colorama import Fore
from colorama import Style
from constants.card_colors import CardColor

NUMBERS = ["1", "2", "3", "4", "5"]

class CardKnowledge:
    def __init__(self):
        self.possible_colors = list(CardColor)
        self.possible_numbers = list(NUMBERS)

    def update_colors(self, matches, color):
        if matches:
            self.possible_colors = color
        else:
            self.possible_colors.replace(color, '')

    def update_numbers(self, matches, number):
        if matches:
            self.possible_numbers = number
        else:
            self.possible_numbers.replace(number, '')


class Card:
    def __init__(self, color: CardColor, number: int):
        self.color = color
        self.number = number
        self.knowledge = CardKnowledge()

    def get_hint(self, hint):
        if hint in CardColor:
            matches = hint == self.color
            self.knowledge.update_colors(matches, hint)
        elif hint in NUMBERS:
            matches = hint == self.number
            self.knowledge.update_numbers(matches, hint)

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
