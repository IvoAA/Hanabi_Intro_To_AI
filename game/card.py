from colorama import Fore
from colorama import Style
from constants.card_colors import CardColor
from typing import Union, List

NUMBERS = [1, 2, 3, 4, 5]

class CardKnowledge:
    """
    Representation of the card knowledge aka. what is known to
    the player and the other players about a given card.
    """
    def __init__(self):
        self.possible_colors = list(CardColor)
        self.possible_numbers = list(NUMBERS)

    def update_colors(self, color: CardColor, matching: bool):
        if len(self.possible_colors) == 1:
            return

        if matching:
            self.possible_colors = [color]
        else:
            if color in self.possible_colors:
                self.possible_colors.remove(color)

    def update_numbers(self, number, matching: bool):
        if len(self.possible_numbers) == 1:
            return

        if matching:
            self.possible_numbers = [number]
        else:
            if number in self.possible_numbers:
                self.possible_numbers.remove(number)

    def __str__(self):
        return f"{''.join(map(str, self.possible_numbers)):<5}|{''.join(list(map(lambda x: x.value[0], self.possible_colors))):<5}"

    def __eq__(self, other):
        return other.possible_colors == self.possible_colors and other.possible_numbers == self.possible_numbers

    def __to_dict__(self):
        return {
            "possible_colors": list(map(lambda x: x.value[0], self.possible_colors)),
            "possible_numbers": self.possible_numbers
        }

    @staticmethod
    def from_dict(dict_object: dict):
        card_knowledge = CardKnowledge()
        card_knowledge.possible_colors = list(map(lambda x: CardColor.from_value(x), dict_object["possible_colors"]))
        card_knowledge.possible_numbers = dict_object["possible_numbers"]
        return card_knowledge


class Card:
    """
    A playing card which is represented by the color and number and its knowledge
    """
    def __init__(self, color: CardColor, number: int):
        self.color = color
        self.number = number
        self.knowledge = CardKnowledge()

    def give_hint(self, hint: Union[CardColor, int]):
        if type(hint) is CardColor:
            self.knowledge.update_colors(hint, hint == self.color)
        elif type(hint) is int:
            self.knowledge.update_numbers(hint, hint == self.number)

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

    def __to_dict__(self):
        return {
            "number": self.number,
            "color": self.color.value[0],
            "knowledge": self.knowledge.__to_dict__()
        }

    def __eq__(self, other):
        if type(other) == tuple and self.color == other[0] and self.number == other[1]:
            return True
        if type(other) == Card and self.color == other.color and self.number == other.number:
            return True
        return False

    @staticmethod
    def from_dict(object_dict: dict):
        new_card = Card(CardColor.from_value(object_dict["color"]), int(object_dict["number"]))
        new_card.knowledge = CardKnowledge.from_dict(object_dict["knowledge"])
        return new_card
