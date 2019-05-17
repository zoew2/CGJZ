import unittest
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    preprocessor = Preprocessor()
    preprocessor.init()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        expected_tokenized_sen= ['-PRON-', 'take', '-PRON-', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor().sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence1 = "In the morning he took his small puppy to New York today ."
        expected_tokenized_sen1 = ['the morning', '-PRON-', 'take', '-PRON-', 'small', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor().sent_preprocessing(raw_sentence1)
        self.assertEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor().sent_preprocessing(raw_sentence2)
        self.assertEqual(expected_tokenized_sen2, tokenized_sen2)





if __name__ == '__main__':
    unittest.main()
