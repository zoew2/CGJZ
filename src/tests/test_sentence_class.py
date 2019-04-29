import unittest
from src.helpers.class_sentence import Sentence


class SentenceClassTests(unittest.TestCase):
    """
    Tests for Sentence class functionality
    """

    def test_process_sentence(self):
        test_sentence = "In a park somewhere, a bunch of puppies played fetch with their owners today."
        doc_id = "TST_ENG_20190101.0001"
        s = Sentence(test_sentence, 0, doc_id)
        a = s.tokenized()
        b = s.word_count()
        c = s.is_first_sentence()
        d = s.position()
        e = s.document_id()

        features = [a, b, c, d, e]
        expected_features = [['in', 'park', 'somewhere', 'bunch', 'puppies', 'played', 'fetch', 'owners', 'today'],
                             14, True, 0, 'TST_ENG_20190101.0001']

        self.assertCountEqual(features, expected_features)


if __name__ == '__main__':
    unittest.main()
