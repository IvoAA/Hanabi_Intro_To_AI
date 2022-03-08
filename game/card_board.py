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
        if self.goal[card.color] == card.number - 1:
            self.goal[card.color] += 1
            return True
        self.discard.append(card)
        return False

    def score(self):
        score = 0
        for point in self.goal.values():
            score += point
        return score

    def __str__(self):
        discard_pile = self._stringy_discard()
        return f"Goal board - {Fore.RED}{self.goal[CardColor.RED]} " \
               f"{Fore.BLUE}{self.goal[CardColor.BLUE]} " \
               f"{Fore.WHITE}{self.goal[CardColor.WHITE]} " \
               f"{Fore.YELLOW}{self.goal[CardColor.YELLOW]} " \
               f"{Fore.GREEN}{self.goal[CardColor.GREEN]} \n" \
            f"{Style.RESET_ALL}Discard pile - {discard_pile}"

    def _stringy_discard(self):
        if len(self.discard) == 0:
            return "[]"
        deck_builder = "[ "
        for card in self.discard:
            deck_builder += f"{str(card)}, "
        deck_builder = deck_builder[:-2]
        deck_builder += " ]"
        return deck_builder
