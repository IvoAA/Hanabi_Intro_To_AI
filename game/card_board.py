from constants.card_colors import CardColor
from colorama import Fore
from game.card import Card


class CardBoard:
    def __init__(self):
        self.goal = {CardColor.RED: 0, CardColor.BLUE: 0, CardColor.WHITE: 0, CardColor.YELLOW: 0, CardColor.GREEN: 0}
        self.discard = []

    def discard_card(self, card: Card):
        self.discard.append(card)

    def play_card(self, card: Card) -> bool:
        if self.goal[card.color] == card.number - 1:
            self.goal[card.color] += 1
            return True
        return False

    def __str__(self):
        return f"Goal board - {Fore.RED}{self.goal[CardColor.RED]} " \
               f"{Fore.BLUE}{self.goal[CardColor.BLUE]} " \
               f"{Fore.WHITE}{self.goal[CardColor.WHITE]} " \
               f"{Fore.YELLOW}{self.goal[CardColor.YELLOW]} " \
               f"{Fore.GREEN}{self.goal[CardColor.GREEN]}"
