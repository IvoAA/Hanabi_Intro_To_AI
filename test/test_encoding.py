import unittest
from game.card import Card, CardKnowledge
from constants.card_colors import CardColor
from game.hand import Hand
from agent.AI.alpha import Alpha
from game.game_board import GameBoard


class TestEncoding(unittest.TestCase):
    def test_full_unknown_encoding(self):
        knowledge = CardKnowledge()
        encoded_knowledge = knowledge.__to_dict__()

        decoded_knowledge = CardKnowledge.from_dict(encoded_knowledge)

        for before, after in zip(knowledge.possible_colors, decoded_knowledge.possible_colors):
            self.assertEqual(before, after)

        for before, after in zip(knowledge.possible_numbers, decoded_knowledge.possible_numbers):
            self.assertEqual(before, after)

    def test_full_known_encoding(self):
        knowledge = CardKnowledge()
        knowledge.update_colors(CardColor.RED, True)
        knowledge.update_numbers(1, True)

        encoded_knowledge = knowledge.__to_dict__()
        decoded_knowledge = CardKnowledge.from_dict(encoded_knowledge)

        for before, after in zip(knowledge.possible_colors, decoded_knowledge.possible_colors):
            self.assertEqual(before, after)

        for before, after in zip(knowledge.possible_numbers, decoded_knowledge.possible_numbers):
            self.assertEqual(before, after)

    def test_card_encoding(self):
        card = Card(CardColor.RED, 1)

        card.give_hint(1)

        encoded_card = card.__to_dict__()

        decoded_card = Card.from_dict(encoded_card)

        self.assertEqual(len(decoded_card.knowledge.possible_numbers), 1)

    def test_hand_encoding(self):

        cards = [Card(CardColor.RED, x) for x in range(1, 5)]
        cards[-1].give_hint(4)
        hand = Hand(cards)
        hand_encoded = hand.__to_list__()

        decoded_hand = Hand.from_list(hand_encoded)
        first_card: Card = list(decoded_hand.cards.values())[-1]
        self.assertEqual(len(first_card.knowledge.possible_numbers), 1)

    def test_game_board_dict(self):
        players = [Alpha(f"{x}", None) for x in range(4)]
        game_board = GameBoard(players)
        game_board.player_hands['0'].cards[1].give_hint(1)

        game_board_dict = game_board.__to_dict__()

        new_game_board = GameBoard.from_dict(game_board_dict, [Alpha for _ in range(4)])

        self.assertEqual(len(game_board.player_hands['0'].cards[1].knowledge.possible_numbers),
                         len(new_game_board.player_hands['0'].cards[1].knowledge.possible_numbers))


if __name__ == '__main__':
    unittest.main()
