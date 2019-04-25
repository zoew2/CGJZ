import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
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
        document = Document("TST_ENG_20190101.0001")

        WordMap.create_mapping()
        vec = Vectors()
        vec.create_freq_vectors({"PUP1A": [document]})
        idf = MeadSummaryGenerator([document], selector).get_idf_array()

        selected = selector.select_content([document], idf)
        selector.apply_redundancy_penalty(selected[0])
        scores = [s.mead_score for s in selector.selected_content[:3]]
        expected_scores = [-0.5, 0.0, -0.07692307692307693]

        self.assertEqual(scores, expected_scores)


if __name__ == '__main__':
    unittest.main()
