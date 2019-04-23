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
        sentence_1 = "Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                     "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                     "as the holy Moslem festival of Eid approaches here."
        sentence_2 = "Kashmiris are known as incorrigible festive shoppers and because of that reputation, " \
                     "unscrupulous shopkeepers have been minting money by over-charging the locals for everything " \
                     "from a chop of mutton to the chickens and hosiery items that the locals must buy to protect " \
                     "themselves from the biting cold of the winter."
        expected_info = [Sentence(sentence_1, 1), Sentence(sentence_2, 2)]

        documents = [Document('XIN_ENG_20041113.0001'), Document('APW_ENG_20041011.0001')]
        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()

        first_sentences = generator.content_selector.selected_content[:2]

        self.assertListEqual(expected_info, first_sentences)

    def test_realize_content(self):
        """
        Test applying redundancy penalty during realize_content
        :return:
        """
        documents = [Document('XIN_ENG_20041113.0001'),
                     Document('APW_ENG_20041011.0001')]
        expected_content = "This measure has obviously been taken to take care of the building tensions between the " \
                           "Indian army and local people who often come into unpleasant contact during encounters, " \
                           "crackdown operations and search and cordon exercises that have become so routine in " \
                           "Kashmir ever since the present armed struggle against the Indian rule started here 18 " \
                           "years back.\nBut, around this Eid festival, there is more to the happy public mood than " \
                           "just the urge to over spend during the festival."

        vec = Vectors()
        WordMap.create_mapping()
        vec.create_freq_vectors({"TestTopic": documents})

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()
        generator.content_selector.selected_content = generator.content_selector.selected_content[:5]
        realized_content = generator.realize_content()

        self.assertEqual(expected_content, realized_content)


if __name__ == '__main__':
    unittest.main()
