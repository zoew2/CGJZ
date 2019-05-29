import unittest
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    Preprocessor.load_models()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        expected_tokenized_sen= ['take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor.sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence1 = "In the morning he took his small puppy to New York today ."
        expected_tokenized_sen1 = ['the morning', 'take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor.sent_preprocessing(raw_sentence1)
        self.assertEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor.sent_preprocessing(raw_sentence2)
        self.assertEqual(expected_tokenized_sen2, tokenized_sen2)

<<<<<<< Updated upstream
        raw_sentence3 = "Washington is New York ."
        expected_tokenized_sen3 = ['Washington', 'New York']

        tokenized_sen3=Preprocessor.sent_preprocessing(raw_sentence3)
        self.assertEqual(expected_tokenized_sen3, tokenized_sen3)
=======
        raw_sentence3 = 'Moreover, it said, it found that some monkeys ' \
                        'given high doses of the drug had developed ' \
                        'potentially serious brain damage.'
>>>>>>> Stashed changes

        raw_sentence4 = 'The U.S. Food and Drug Administration is slated ' \
                        'to rule on whether to approve Arcoxia by Oct. 30, ' \
                        'but most analysts and doctors don\'t believe the ' \
                        'agency will act without longer safety studies.'

        raw_sentence5 = 'The key issue in the legal action to be filed ' \
                        'Wednesday is nitrogen, which along with phosphorus ' \
                        'serves as food for huge algae blooms in the bay.'

        raw_sentence6 = 'John Hathcock, of the Washington, D.C.-based dietary ' \
                        'supplement industry group, the Council for Responsible ' \
                        'Nutrition, said the industry does not oppose warning labels,' \
                        ' but he dismissed suggestions that ephedra products ought to ' \
                        'be sold by prescription only.'

        test_sentences = [raw_sentence3, raw_sentence4, raw_sentence5, raw_sentence6]

        for s in test_sentences:
            print(Preprocessor.sent_preprocessing(s))


if __name__ == '__main__':
    unittest.main()
