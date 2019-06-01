import unittest
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    Preprocessor.load_models()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        processed = Preprocessor.get_processed_sentence(raw_sentence)
        expected_tokenized_sen= ['take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor.get_processed_tokens(processed)
        self.assertCountEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence1 = "In the morning he took his small puppy to New York today ."
        processed1 = Preprocessor.get_processed_sentence(raw_sentence1)
        expected_tokenized_sen1 = ['the morning', 'take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor.get_processed_tokens(processed1)
        self.assertCountEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        processed2 = Preprocessor.get_processed_sentence(raw_sentence2)
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor.get_processed_tokens(processed2)
        self.assertCountEqual(expected_tokenized_sen2, tokenized_sen2)

        raw_sentence3 = "Washington is New York ."
        expected_tokenized_sen3 = ['Washington', 'New York']

        tokenized_sen3=Preprocessor.sent_preprocessing(raw_sentence3)
        self.assertEqual(expected_tokenized_sen3, tokenized_sen3)




if __name__ == '__main__':
    unittest.main()
