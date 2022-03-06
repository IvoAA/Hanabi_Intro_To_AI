from game.action import Action, PLAY, DISCARD, HINT
from constants.player_type import PlayerType
from game.game_board import GameBoard


class Player:
    def __init__(self, player_type: PlayerType, player_id: str):
        if player_type not in PlayerType:
            raise Exception('Please select a valid agent type')

        self.player_type = player_type
        self.player_id = player_id
        self.game_board = None

    def link_game_board(self, game_board: GameBoard):
        self.game_board = game_board

    def play(self):
        if self.player_type == PlayerType["HUMAN"]:
            print(f"Please select an action type:")

            action_types = {
                'P': PLAY,
                'D': DISCARD
            }
            if self.game_board.has_coins():
                action_types['H'] = HINT
            action_type = None

            for k, v in action_types.items():
                print(f"{k}: {v}")

            while not action_type:
                a_type = input().upper()
                if a_type in action_types:
                    action_type = action_types[a_type]
                    continue

                print('Please choose a valid action type:')
                for k, v in action_types.items():
                    print(f"{k}: {v}")

            possible_actions = Action.get_possible_actions(self.game_board, self.player_id, action_type)
            print(f"Please select an action: {possible_actions}")  # TODO proper display of actions
            action_id = input()

            return Action(action_type, action_id)

        # TODO easy way to implement several types of agents and compare them, in case we want it in the future
        elif self.player_type == PlayerType["AI"]:
            pass

    def print_view(self):
        player = self.game_board
        print("Printing game state.")
        print()

    def to_str(self):
        return f"Id:{self.player_id}\tType:{self.player_type}"
