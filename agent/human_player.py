import traceback
from typing import Union

from agent.player import Player
from constants.card_colors import CardColor
from game.game_board import GameBoard


class HumanPlayer(Player):
    def __init__(self, player_id: str, game_board: GameBoard):
        super().__init__(player_id, game_board)

    def play(self):
        print(f"Player {self.player_id} turn. Make a play.")
        try:
            command = self._print_Plays()
            if command[0] == 'P':
                self.play_card(int(command[1]) - 1)
            if command[0] == 'H':
                hinted_card = self.game_board.player_hands[command[1]].get_card_by_idx(int(command[2]) - 1)
                hint = self._map_hint(command[3])
                hinted_card.give_hint(hint)
            if command[0] == 'D':
                if not self.discard_card(self.hand.cards[int(command[1])]):
                    print("Cant discard a card when you have max coins.")
                    self.play()
        except:
            traceback.print_exc()
            print('Error on input, try again')
            self.play()

    def _print_Plays(self) -> list:
        print()
        print("#################################################################")
        print("Type 'P' for playing a card followed by the card number (ex. P 3)")
        print("Type 'H' for hinting a card, followed by player name card number "
              "and Color (R, B, W, Y, G) or number (1-4) (ex. H Turing 3 B)")
        print("Type 'D' for discarding a card and getting a coin (ex. D 3)")
        command = input("Enter option ... followed by enter").split()
        return command

    def _map_hint(self, hint: str) -> Union[CardColor, int]:
        if hint == 'R':
            return CardColor.RED
        if hint == 'B':
            return CardColor.BLUE
        if hint == 'W':
            return CardColor.WHITE
        if hint == 'Y':
            return CardColor.YELLOW
        if hint == 'G':
            return CardColor.GREEN
        return int(hint)
