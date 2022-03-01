import os

from game.game_board import GameBoard
from game.player import Player, PLAYER_TYPES

INIT = 0
SELECT_N_PLAYERS = 1
INITIATE_PLAYERS = 2
GAME_STARTED = 3
GAME_FINISHED = 4


class GameEngine:

    def __init__(self):
        self.state = INIT
        self.n_players = self.select_n_players()
        self.print_game_state()
        self.players = self.initiate_players()

        self.game_board = GameBoard(self.players)

        self.start_game()

    def select_n_players(self):
        self.state = SELECT_N_PLAYERS
        print('Please insert the intended number of players (2 - 5)')
        print('(default = 4)\n')
        n_players = input()
        try:
            n_players = n_players if (1 < int(n_players) < 6) else 4
        except ValueError:
            n_players = 4

        return int(n_players)

    def initiate_players(self):
        self.state = INITIATE_PLAYERS
        # select player types (maybe give them names/ids so they're easier to identify?)
        players = []
        for i in range(1, self.n_players + 1):
            print(f"Please insert the type for Player {i}")
            print(f"(default = {PLAYER_TYPES[0]})\n")
            for j, p_type in enumerate(PLAYER_TYPES):
                print(f"{j}: {p_type}")

            player_type = PLAYER_TYPES[0]
            try:
                player_type = PLAYER_TYPES[int(input())]
            except:
                pass

            print(f"Please insert the name for Player {i}")
            print(f"(default = Player {i})\n")

            # TODO check that id is not used before
            player_id = input() or f"Player {i}"

            new_player = Player(player_type, player_id)
            players.append(new_player)

            print(f"New player created:\t{new_player.to_str()}")
        return players

    def start_game(self):
        curr_player = 0

        while not self.game_board.finished:
            curr_action = self.players[curr_player].play(self.game_board)

            self.game_board.play_action(curr_player, curr_action)

            curr_player = (curr_player + 1) % self.n_players

    def print_game_state(self):
        print('\n'*100)

        pass
