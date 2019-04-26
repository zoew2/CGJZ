import unittest
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap


class WordMapTests(unittest.TestCase):
    """
    tests for WordMap
    """

    def test_create_mapping(self):
        doc1 = Document("TST_ENG_20190101.0001")
        doc2 = Document("TST_ENG_20190101.0002")

        all_words = set()
        for document in [doc1, doc2]:
            for sentence in document.sens:
                all_words = all_words.union(sentence.tokens)

        WordMap.create_mapping()
        mapping = WordMap.get_mapping()

        self.assertEqual(all_words, mapping.keys())  # each unique word in input got added to the dictionary
        self.assertEqual(len(mapping), len(set(mapping.items())))  # each id value in the dict is unique


if __name__ == '__main__':
    unittest.main()
