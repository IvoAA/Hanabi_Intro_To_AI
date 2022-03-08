from colorama import Fore
from colorama import Style
from constants.card_colors import CardColor
from typing import Union


NUMBERS = [1, 2, 3, 4, 5]

class CardKnowledge:
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
        return f"{''.join(map(str, self.possible_numbers))}|{''.join(list(map(lambda x: x.value[0], self.possible_colors)))}"

    def __encode__(self):
        return f"[{str(self)}]"

    @staticmethod
    def decode(encoded_information: str):
        encoded_information = encoded_information.replace("[", "")
        encoded_information = encoded_information.replace("]", "")

        numbers_str, colors_str = encoded_information.split("|")

        numbers = list(map(int, numbers_str))
        colors = list(map(lambda x: CardColor.from_value(x), colors_str))

        card_knowledge = CardKnowledge()
        card_knowledge.possible_colors = colors
        card_knowledge.possible_numbers = numbers
        return card_knowledge


class Card:
    def __init__(self, color: CardColor, number: int):
        self.color = color
        self.number = number
        self.knowledge = CardKnowledge()

    def give_hint(self, hint: Union[CardColor, int]):
        if isinstance(hint, CardColor):
            self.knowledge.update_colors(hint, hint == self.color)
        elif isinstance(hint, int):
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

    def __encode__(self):
        return f"[{str(self.color.value[0])}|{str(self.number)}|{self.knowledge.__encode__()}]"

    @staticmethod
    def decode(encoded_information: str):
        if encoded_information[0] == "[":
            encoded_information = encoded_information[1:]
        if encoded_information[-1] == "]":
            encoded_information = encoded_information[:-1]

        color_str, number_str, knowledge_information_encoded = encoded_information.split("|", 2)

        decoded_card = Card(CardColor.from_value(color_str), int(number_str))
        decoded_knowledge = CardKnowledge.decode(knowledge_information_encoded)
        decoded_card.knowledge = decoded_knowledge

        return decoded_card
