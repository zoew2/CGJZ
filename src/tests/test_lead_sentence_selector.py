import unittest
from src.lead_sentence_selector import LeadSentenceSelector
from src.class_document import Document
from src.class_sentence import Sentence


class LeadSentenceSelectorTests(unittest.TestCase):
    """
    Tests for LeadSentenceSelector
    """

    def test_select_content(self):
        sentence_1 = "Describe the debate over use of emergency contraceptives, " \
                     "also called the morning-after pill, and whether or not it should " \
                     "be available without a prescription."
        doc_id_1 = 'XIN_ENG_20041113.0001'
        sentence_2 = "Today is Friday, October 8, the 281st day of 2004."
        doc_id_2 = 'APW_ENG_20041001.0001'

        selector = LeadSentenceSelector()
        documents = [Document(doc_id_1), Document(doc_id_2)]
        expected_sentences = [Sentence(sentence_1, 1, doc_id_1), Sentence(sentence_2, 2, doc_id_2)]
        selected_sentences = selector.select_content(documents)

        self.assertEqual(expected_sentences, selected_sentences)


if __name__ == '__main__':
    unittest.main()
