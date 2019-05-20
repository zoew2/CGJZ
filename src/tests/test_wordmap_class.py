import unittest
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
from src.helpers.class_preprocessor import Preprocessor


class WordMapTests(unittest.TestCase):
    """
    tests for WordMap
    """

    word_set = {'hang', 'park', 'small', 'fetch', 'run', 'load', 'dog', 'together', 'love', 'get', 'fun', 'tail', 'play', 'playing', 'owner', 'chase', 'bunch', 'toy', 'like', 'today', 'take', 'big', 'puppy', 'sun', 'tongue', 'wag', 'around', 'fight', 'many', 'somewhere'}

    def test_create_mapping(self):

        Preprocessor.load_models()

        WordMap.word_set = set()
        WordMap.word_to_id = {}

        Document("TST_ENG_20190101.0001")
        Document("TST_ENG_20190101.0002")

        WordMap.create_mapping()
        mapping = WordMap.get_mapping()

        self.assertCountEqual(self.word_set, mapping.keys())  # each word in word_set got added to the dictionary
        self.assertEqual(len(mapping), len(set(mapping.items())))  # each id value in the dict is unique


if __name__ == '__main__':
    unittest.main()
