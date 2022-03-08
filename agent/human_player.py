import traceback
from typing import Union

from agent.player import Player
from constants.card_colors import CardColor
from game.game_board import GameBoard


class HumanPlayer(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)

    def play(self):
        print(f"Player {self.player_id} turn. Make a play.")
        try:
            command_args = self._print_plays()
            if command_args[0] == 'P':
                number_of_card_to_play = command_args[1]
                self.play_card(int(number_of_card_to_play))
                return
            if command_args[0] == 'H':
                hint_for_player = command_args[1]
                raw_hint = command_args[2]
                hint = self._map_hint(raw_hint)
                for card in self.game_board.player_hands[hint_for_player].cards.values():
                    card.give_hint(hint)
                return
            if command_args[0] == 'D':
                number_of_card_to_play = command_args[1]
                if not self.discard_card(int(number_of_card_to_play)):
                    print("Cant discard a card when you have max coins.")
                    self.play()
                return
            print("Error on input, try again")
            self.play()
        except:
            traceback.print_exc()
            print('Error on input, try again')
            self.play()

    def _print_plays(self) -> list:
        print()
        print("#################################################################")
        print("Type 'P' for playing a card followed by the card number (ex. P 3)")
        print("Type 'H' for hinting a card, and Color (R, B, W, Y, G) or number "
              "(1-4) (ex. H Turing 3 B)")
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
