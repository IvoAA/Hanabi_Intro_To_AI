from game.action import Action, ACTION_TYPES

HUMAN = 'HUMAN'
AI_AGENT = 'AI_AGENT'

PLAYER_TYPES = [AI_AGENT, HUMAN]

class Player:
    def __init__(self, agent_type):
        if agent_type not in PLAYER_TYPES:
            raise Exception('Please select a valid agent type')

        self.agent_type = agent_type

    def play(self, game_board):
        if self.agent_type == HUMAN:
            print(f"Please select an action type: {ACTION_TYPES}")
            action_type = None

            while not action_type:
                a_type = input()
                action_type = ACTION_TYPES.get(a_type, None)

            possible_actions = Action.get_possible_actions(game_board, action_type)
            print(f"Please select an action: {possible_actions}")
            action_id = input()

            return Action(action_type, action_id)

        # TODO easy way to implement several types of agents and compare them, in case we want it in the future
        elif self.agent_type == AI_AGENT:
            pass
