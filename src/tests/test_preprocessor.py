import unittest
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    preprocessor = Preprocessor()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        expected_tokenized_sen= ['-PRON-', 'take', '-PRON-', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor().sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence = "In the morning he took his small puppy to New York today ."
        expected_tokenized_sen = ['the morning', '-PRON-', 'take', '-PRON-', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor().sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)



if __name__ == '__main__':
    unittest.main()
