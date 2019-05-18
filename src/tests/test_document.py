import unittest
from src.helpers.class_document import Document
from src.helpers.class_preprocessor import Preprocessor


class DocumentTests(unittest.TestCase):
    """
    Tests for Document class
    """

    Preprocessor.load_models()

    def test_parse_doc_id(self):
        doc = Document("TST_ENG_20190101.0001")
        self.assertEqual(doc.src, 'TST')
        self.assertEqual(doc.lang, '_ENG')
        self.assertEqual(doc.date, '20190101')
        self.assertEqual(doc.art_id, '0001')
        self.assertEqual(doc.docid, 'TST_ENG_20190101.0001')

    def test_parse_doc_id2(self):
        doc = Document("TST20190201.0001")
        self.assertEqual(doc.src, 'TST')
        self.assertEqual(doc.lang, '_ENG')
        self.assertEqual(doc.date, '20190201')
        self.assertEqual(doc.art_id, '0001')
        self.assertEqual(doc.docid, 'TST20190201.0001')

    def test_document_headline(self):
        doc = Document("TST_ENG_20190101.0001")
        self.assertEqual(doc.headline, "Puppies play fetch in the park")

    def test_document_headline2(self):
        doc = Document("TST_ENG_20190101.0002")
        self.assertEqual(doc.headline, "Playing in the dog park")


if __name__ == '__main__':
    unittest.main()
