import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors


class MeadSentenceSelectorTests(unittest.TestCase):
    """
    Tests for MeadContentSelector
    """

    def test_apply_redundancy_penalty(self):
        """
        Test the function to apply the redundancy penalty
        :return:
        """
        selector = MeadContentSelector()
        document = Document("APW_ENG_19980613.0001")

        vec = Vectors()
        WordMap.create_mapping()
        vec.create_freq_vectors({"TestTopic": [document]})

        selector.select_content([document])
        selector.apply_redundancy_penalty(selector.selected_content[0])
        scores = [s.mead_score for s in selector.selected_content[:3]]
        expected_scores = [0.5, 0.97222222222222221, 1.0]

        self.assertEqual(scores, expected_scores)


if __name__ == '__main__':
    unittest.main()
