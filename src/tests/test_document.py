import unittest
from src.class_document import Document


class DocumentTests(unittest.TestCase):
    """
    Tests for Document class
    """

    def test_parse_doc_id(self):
        newdoc = Document("APW_ENG_19980613.0001")
        self.assertEqual(newdoc.src, 'APW')
        self.assertEqual(newdoc.lang, 'ENG')
        self.assertEqual(newdoc.date, '19980613')
        self.assertEqual(newdoc.art_id, '0001')
        self.assertEqual(newdoc.docid, 'APW_ENG_19980613.0001')
        self.assertEqual(newdoc.docid_inxml, 'APW19980613.0001')


if __name__ == '__main__':
    unittest.main()
