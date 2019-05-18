import unittest
from src.lead_sentence.lead_sentence_selector import LeadSentenceSelector
from src.lead_sentence.lead_summary_generator import LeadSummaryGenerator
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.helpers.class_preprocessor import Preprocessor


class LeadSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for LeadSummaryGenerator
    """

    Preprocessor.load_models()

    def test_order_information(self):
        sentence_1 = 'Puppies are cute because many of them are small.'
        doc_id_1 = 'TST20190201.0001'
        sentence_2 = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        doc_id_2 = 'TST_ENG_20190101.0001'
        expected_info = [Sentence(sentence_2, 1, doc_id_2), Sentence(sentence_1, 1, doc_id_1)]

        documents = [Document('TST_ENG_20190101.0001'), Document('TST20190201.0001')]
        generator = LeadSummaryGenerator(documents, LeadSentenceSelector(), [])
        generator.select_content()
        generator.order_information()

        self.assertListEqual(expected_info, generator.content_selector.selected_content)

    def test_realize_content(self):
        documents = [Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002')]
        expected_content = "In a park somewhere, a bunch of puppies played fetch with their owners today.\n" \
                           "I took my small puppy to the dog park today.\n" \
                           "Puppies are cute because many of them are small.\n" \
                           "Puppies love to play with toys."

        generator = LeadSummaryGenerator(documents, LeadSentenceSelector(), [])
        generator.select_content()
        generator.order_information()
        realized_content = generator.realize_content()
        self.assertEqual(expected_content, realized_content)

    def test_lead_summary_length(self):
        documents = [Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002'),
                     Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002')]
        max_length = 100

        generator = LeadSummaryGenerator(documents, LeadSentenceSelector(), [])
        generator.select_content()
        generator.order_information()
        realized_content = generator.realize_content()
        content_length = len(realized_content.split(" "))
        self.assertLessEqual(content_length, max_length)


if __name__ == '__main__':
    unittest.main()
