from enum import Enum


class CardColor(Enum):
    RED = 'R',
    BLUE = 'B',
    WHITE = 'W',
    YELLOW = 'Y',
    GREEN = 'G'

    @staticmethod
    def from_value(value: str):
        if value == 'R':
            return CardColor.RED
        elif value == 'B':
            return CardColor.BLUE
        elif value == 'W':
            return CardColor.WHITE
        elif value == 'Y':
            return CardColor.YELLOW
        elif value == 'G':
            return CardColor.GREEN

