import unittest
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap


class WordMapTests(unittest.TestCase):
    """
    tests for WordMap
    """

    word_set = {'in', 'a', 'park', 'puppies', 'bone', 'tails', 'with', 'fetch', 'wagging', 'their',
                'hanging', 'loads'}

    def test_create_mapping(self):
        WordMap.create_mapping()
        mapping = WordMap.get_mapping()

        self.assertEqual(self.word_set, mapping.keys())  # each word in word_set got added to the dictionary
        self.assertEqual(len(mapping), len(set(mapping.items())))  # each id value in the dict is unique


if __name__ == '__main__':
    unittest.main()
