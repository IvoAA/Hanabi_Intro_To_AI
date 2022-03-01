PLAY = 'PLAY'
DISCARD = 'DISCARD'
HINT = 'HINT'

ACTION_TYPES = [PLAY, DISCARD, HINT]


class Action:
    def __init__(self, action_type, action_id):
        # TODO maybe subclasses for each action type?
        # HINT needs to be treated differently
        self.action_type = action_type
        self.action_id = action_id

    @staticmethod
    def get_possible_actions(cls, game_board, action_type):
        # TODO return a prettier result

        # use game_board to see how many cards we can play/discard, as I assume that in the end game each player has
        # less cards in their hand (I could be wrong)
        if action_type == PLAY:
            return [range(1, 6)]
        elif action_type == DISCARD:
            return [range(1, 6)]
        if action_type == HINT:
            # use game board to see which hints (if any) can be given
            return [range(1, 6)]
