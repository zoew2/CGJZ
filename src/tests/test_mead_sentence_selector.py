import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.helpers.class_sentence import Sentence


class MeadSentenceSelectorTests(unittest.TestCase):
    """
    Tests for MeadContentSelector
    """

    def test_apply_redundancy_penalty(self):
        selector = MeadContentSelector()
        sentence1 = Sentence('This is a test', 1)
        sentence1.mead_score = 1.0
        sentence2 = Sentence('This is also a test', 2)
        sentence2.mead_score = 1.0
        sentence3 = Sentence('Wow what a difference sentence', 3)
        sentence3.mead_score = 1.0

        selector.selected_content = [sentence1, sentence2, sentence3]

        selector.apply_redundancy_penalty(sentence1)
        scores = [s.mead_score for s in selector.selected_content]
        expected_scores = [1.0, 1.0, 1.0]

        self.assertEqual(scores, expected_scores)


if __name__ == '__main__':
    unittest.main()
