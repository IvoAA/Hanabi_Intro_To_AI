import unittest
from game.card import Card, CardKnowledge
from constants.card_colors import CardColor


class TestEncoding(unittest.TestCase):
    def test_full_unknown_encoding(self):
        knowledge = CardKnowledge()
        encoded_knowledge = knowledge.__encode__()

        decoded_knowledge = CardKnowledge.decode(encoded_knowledge)

        for before, after in zip(knowledge.possible_colors, decoded_knowledge.possible_colors):
            self.assertEqual(before, after)

        for before, after in zip(knowledge.possible_numbers, decoded_knowledge.possible_numbers):
            self.assertEqual(before, after)

    def test_full_known_encoding(self):
        knowledge = CardKnowledge()
        knowledge.update_colors(CardColor.RED, True)
        knowledge.update_numbers(1, True)

        encoded_knowledge = knowledge.__encode__()
        decoded_knowledge = CardKnowledge.decode(encoded_knowledge)

        for before, after in zip(knowledge.possible_colors, decoded_knowledge.possible_colors):
            self.assertEqual(before, after)

        for before, after in zip(knowledge.possible_numbers, decoded_knowledge.possible_numbers):
            self.assertEqual(before, after)

    def test_card_encoding(self):

        card = Card(CardColor.RED, 1)

        print(card.__encode__())
        card.give_hint(1)

        encoded_card = card.__encode__()

        decoded_card = Card.decode(encoded_card)

        self.assertEqual(len(decoded_card.knowledge.possible_numbers), 1)



if __name__ == '__main__':
    unittest.main()
