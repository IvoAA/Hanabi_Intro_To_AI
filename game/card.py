RED = 'R'
BLUE = 'B'
WHITE = 'W'
YELLOW = 'Y'
GREEN = 'G'

COLORS = [RED, BLUE, WHITE, YELLOW, GREEN]
NUMBERS = ["1", "2", "3", "4", "5"]


class CardKnowledge:
    def __init__(self):
        self.possible_colors = "".join(COLORS)
        self.possible_numbers = "".join(NUMBERS)

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
    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.knowledge = CardKnowledge()

    def get_hint(self, hint):
        if hint in COLORS:
            matches = hint == self.color
            self.knowledge.update_colors(matches, hint)
        elif hint in NUMBERS:
            matches = hint == self.number
            self.knowledge.update_numbers(matches, hint)