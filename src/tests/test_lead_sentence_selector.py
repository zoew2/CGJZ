import unittest
from src.lead_sentence.lead_sentence_selector import LeadSentenceSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence


class LeadSentenceSelectorTests(unittest.TestCase):
    """
    Tests for LeadSentenceSelector
    """

    def test_select_content(self):
        sentence_1 = "Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                     "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                     "as the holy Moslem festival of Eid approaches here."
        doc_id_1 = 'XIN_ENG_20041113.0001'
        sentence_2 = "Today is Friday, October 8, the 281st day of 2004."
        doc_id_2 = 'APW_ENG_20041001.0001'

        selector = LeadSentenceSelector()
        documents = [Document(doc_id_1), Document(doc_id_2)]
        expected_sentences = {'200410010001': Sentence(sentence_1, 1, doc_id_1),
                              '200411130001': Sentence(sentence_2, 2, doc_id_2)}
        selector.select_content(documents)
        selected_sentences = selector.selected_content

        self.assertCountEqual(expected_sentences, selected_sentences)


if __name__ == '__main__':
    unittest.main()
