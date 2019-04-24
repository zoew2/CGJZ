import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors


class MeadSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for LeadSummaryGenerator
    """

    def test_order_information(self):
        """
        Test ordering Sentences by MEAD score
        :return:
        """
        doc_id_1 = 'TST_ENG_20190101.0001'
        sentence_1 = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        sentence_2 = 'They all ran around with their tails wagging ' \
                     'and their tongues hanging out having loads of fun in the sun.'
        sentence_3 = 'Puppies love playing fetch.'
        expected_info = [Sentence(sentence_1, 1, doc_id_1),
                         Sentence(sentence_3, 3, doc_id_1),
                         Sentence(sentence_2, 2, doc_id_1)]

        documents = [Document('TST_ENG_20190101.0001')]

        ## This is hardcoded until Julia's code is merged
        documents[0].sens[0].mead_score = 0.8
        documents[0].sens[0].order_by = -0.8
        documents[0].sens[1].mead_score = 0.2
        documents[0].sens[1].order_by = -0.2
        documents[0].sens[2].mead_score = 0.5
        documents[0].sens[2].order_by = -0.5

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()

        self.assertListEqual(expected_info, generator.content_selector.selected_content)

    def test_realize_content(self):
        """
        Test applying redundancy penalty during realize_content
        :return:
        """
        expected_content = "Puppies are cute because many of them are small.\n" \
                           "I took my small puppy to the dog park today.\n" \
                           "They all ran around with their tails wagging and their tongues hanging out having loads " \
                           "of fun in the sun.\n" \
                           "Puppies love playing fetch.\n"\
                           "In a park somewhere, a bunch of puppies played fetch with their owners today."

        documents = [Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002')]

        ## This is hardcoded until Julia's code is merged
        documents[0].sens[0].mead_score = 0.8
        documents[0].sens[0].order_by = -0.8
        documents[0].sens[1].mead_score = 0.2
        documents[0].sens[1].order_by = -0.2
        documents[0].sens[2].mead_score = 0.5
        documents[0].sens[2].order_by = -0.5

        WordMap.create_mapping()
        vec = Vectors()
        vec.create_freq_vectors({"PUP1A": documents})

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()
        generator.content_selector.selected_content = generator.content_selector.selected_content[:5]
        realized_content = generator.realize_content()

        self.assertEqual(expected_content, realized_content)


if __name__ == '__main__':
    unittest.main()
