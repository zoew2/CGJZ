import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document


class MeadSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for LeadSummaryGenerator
    """

    def test_order_information(self):
        sentence_1 = "Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                     "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                     "as the holy Moslem festival of Eid approaches here."
        doc_id_1 = 'XIN_ENG_20041113.0001'
        sentence_2 = "The race to claim the five World Cup finals berths from Africa " \
                     "is no clearer after this weekend\'s qualifying matches, " \
                     "but Mexico and Trinidad and Tobago closed in on the final group " \
                     "stage in the CONCACAF region Sunday."
        doc_id_2 = 'APW_ENG_20041001.0001'
        expected_info = [Sentence(sentence_2, 2, doc_id_2), Sentence(sentence_1, 1, doc_id_1)]

        documents = [Document('XIN_ENG_20041113.0001'), Document('APW_ENG_20041011.0001')]
        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()

        self.assertListEqual(expected_info, generator.content_selector.selected_content)

    def test_realize_content(self):
        documents = [Document('XIN_ENG_20041113.0001'),
                     Document('APW_ENG_20041011.0001'),
                     Document('APW_ENG_20041011.0002'),
                     Document('APW_ENG_20041011.0003')]
        expected_content = "Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                           "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                           "as the holy Moslem festival of Eid approaches here.\n" \
                           "Today is Monday, October 18, the 291st day of 2004.\n" \
                           "The race to claim the five World Cup finals berths from Africa " \
                           "is no clearer after this weekend's qualifying matches, " \
                           "but Mexico and Trinidad and Tobago closed in on the final " \
                           "group stage in the CONCACAF region Sunday."

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()
        realized_content = generator.realize_content()

        self.assertEqual(expected_content, realized_content)


if __name__ == '__main__':
    unittest.main()
