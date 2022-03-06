import os

from game.game_board import GameBoard
from constants.player_type import PlayerType
from agent.human_player import HumanPlayer
from agent.AI.alpha import Alpha
import utils.screen as Screen

INIT = 0
SELECT_N_PLAYERS = 1
INITIATE_PLAYERS = 2
GAME_STARTED = 3
GAME_FINISHED = 4


class GameEngine:
    def __init__(self):
        self.game_board = None
        self.state = INIT
        self.n_players = 0
        self.players = []
        self.load_players()
        self.game_board = GameBoard(self.players)
        for player in self.players:
            player.game_injection(self.game_board)

    def load_players(self):
        self.n_players = int(os.environ['NR_PLAYERS'])
        if self.n_players >= 5 or self.n_players <= 2:
            raise "Players value out of bounds. (allowed 3-5 players)"

        for i in range(1, self.n_players + 1):
            p_type = PlayerType[os.environ[f"PLAYER_{i}"]]
            p_name = os.environ[f"PLAYER_{i}_NAME"]
            if p_type == PlayerType.HUMAN:
                self.players.append(HumanPlayer(p_name, self.game_board))
            elif p_type == PlayerType.ALPHA:
                self.players.append(Alpha(p_name, self.game_board))
        self.state = INITIATE_PLAYERS

    def start_game(self):
        curr_player = 0

        while not self.game_board.finished:
            self.print_game_state()
            self.players[curr_player].play()
            curr_player = (curr_player + 1) % self.n_players

    def print_game_state(self):
        Screen.clear_screen()
        self.game_board.view()
