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

        raw_sentence1 = "In the morning he took his new puppy to New York today ."
        processed1 = Preprocessor.get_processed_sentence(raw_sentence1)
        expected_tokenized_sen1 = ['the morning', 'take', 'new', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor.get_processed_tokens(processed1)
        self.assertCountEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        processed2 = Preprocessor.get_processed_sentence(raw_sentence2)
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor.get_processed_tokens(processed2)
        self.assertCountEqual(expected_tokenized_sen2, tokenized_sen2)





    def test_strip_beginning(self):


        raw_sent1 = "*Friday, Feb. 26, 1999 Iranians Vote in Local Elections TEHRAN, Iran (AP) -- Iranians cast ballots today in the nation’s first election of local officials in 20 years."
        result = Preprocessor.strip_beginning(raw_sent1)
        self.assertEqual(result, "Iranians cast ballots today in the nation’s first election of local officials in 20 years.")


        raw_sent2 = "JAKARTA, November 19 (Xinhua) -- Local people and students in Indonesia’s capital Jakarta held an anti-Soeharto mass demonstration, starting at 14:00 local time on Thursday."
        result = Preprocessor.strip_beginning(raw_sent2)
        self.assertEqual(result,
                         "Local people and students in Indonesia’s capital Jakarta held an anti-Soeharto mass demonstration, starting at 14:00 local time on Thursday.")


if __name__ == '__main__':
    unittest.main()
