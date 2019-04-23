import unittest
from src.helpers.class_sentence import Sentence
from src.mead.mead_content_selector import MeadContentSelector


class MeadContentSelectorTests(unittest.TestCase):
    """
    Tests for MeadContentSelector
    """

    def test_get_sentence_position(self):
        sentence_1 = Sentence("Today is Friday, October 8, the 281st day of 2004.", 0)
        sentence_2 = Sentence("Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                     "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                     "as the holy Moslem festival of Eid approaches here.", 50)

        pos_score_1 = MeadContentSelector.get_sentence_position(sentence_1, 100)
        pos_score_2 = MeadContentSelector.get_sentence_position(sentence_2, 100)

        expected_score_1 = 1
        expected_score_2 = 50/100

        self.assertCountEqual(expected_score_1, pos_score_1)
        self.assertEqual(expected_score_2, pos_score_2)


    # def test_get_centroid_score(self):




if __name__ == '__main__':
    unittest.main()
