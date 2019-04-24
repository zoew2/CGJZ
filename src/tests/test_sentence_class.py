import unittest
from src.helpers.class_sentence import Sentence


class SentenceClassTests(unittest.TestCase):
    """
    Tests for Sentence class functionality
    """

    def test_process_sentence(self):
        test_sentence = "Describe the debate over use of emergency contraceptives, " \
               "also called the morning-after pill, and whether or not it should " \
               "be available without a prescription."
        doc_id = "XIN_ENG_20041113.0001"
        s = Sentence(test_sentence, 0, doc_id)
        a = s.tokenized()
        b = s.word_count()
        c = s.is_first_sentence()
        d = s.position()
        e = s.document_id()

        features = [a, b, c, d, e]
        expected_features = [['Describe', 'debate', 'use', 'emergency', 'contraceptives',
                              'also', 'called', 'morning-after', 'pill', 'whether', 'available',
                              'without', 'prescription'],
                             24, True, 0, 'XIN_ENG_20041113.0001']

        self.assertCountEqual(features, expected_features)

        # Todo: test the stemming (need the spacy package), spacy will take care of the tokenization
        # too, but seems to behave not as good as expected? it tokenized morining-after to morning - after
        # then said 'morning' is a name entity, sigh* will looking into that

if __name__ == '__main__':
    unittest.main()
