import unittest
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document


class WordMapTests(unittest.TestCase):
    """
    tests for WordMap
    """

    word_set = {'small', 'tails', 'together', 'somewhere', 'sun', 'dog', 'love', 'chased', 'played', "n't", 'in', 'toys', 'park', 'bunch', 'puppies', 'hanging', 'many', 'owners', 'get', 'fetch', 'loads', 'loves', 'liked', 'dogs', 'fight', 'ran', 'fun', 'took', 'wagging', 'bigger', 'playing', 'they', 'he', 'i', 'tongues', 'around', 'today', 'run', 'there', 'puppy'}

    def test_create_mapping(self):
        WordMap.word_set = set()
        WordMap.word_to_id = {}

        Document("TST_ENG_20190101.0001")
        Document("TST_ENG_20190101.0002")

        WordMap.create_mapping()
        mapping = WordMap.get_mapping()

        self.assertEqual(self.word_set, mapping.keys())  # each word in word_set got added to the dictionary
        self.assertEqual(len(mapping), len(set(mapping.items())))  # each id value in the dict is unique


if __name__ == '__main__':
    unittest.main()
