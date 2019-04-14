import unittest
from src.document import Document


class DocumentTests(unittest.TestCase):
    """
    Tests for Document class
    """

    def test_parse_doc_id(self):
        newdoc = Document("APW_ENG_19980613.0001")
        self.assertEqual(newdoc.src, 'APW')


if __name__ == '__main__':
    unittest.main()
