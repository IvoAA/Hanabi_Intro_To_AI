import random

from agent.player import Player
from game.game_board import GameBoard


class Alpha(Player):
    def __init__(self, player_id: str):
        super().__init__(player_id)

    def play(self):
        print(f"Turn of {self.player_id}")
        input("Press enter to execute random task")
        # idx starts always with zero
        card_idx = random.randint(0, 3)
        self.play_card(card_idx)

