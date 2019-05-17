import unittest
from src.lead_sentence.lead_sentence_selector import LeadSentenceSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence


class LeadSentenceSelectorTests(unittest.TestCase):
    """
    Tests for LeadSentenceSelector
    """

    def test_select_content(self):
        sentence_1 = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        doc_id_1 = 'TST_ENG_20190101.0001'
        sentence_2 = 'I took my small puppy to the dog park today.'
        doc_id_2 = 'TST_ENG_20190101.0002'

        selector = LeadSentenceSelector()
        documents = [Document(doc_id_1), Document(doc_id_2)]
        expected_sentences = [Sentence(sentence_1, 1, doc_id_1), Sentence(sentence_2, 1, doc_id_2)]
        selector.select_content(documents, [])
        selected_sentences = selector.selected_content

        self.assertCountEqual(expected_sentences, selected_sentences)


if __name__ == '__main__':
    unittest.main()
