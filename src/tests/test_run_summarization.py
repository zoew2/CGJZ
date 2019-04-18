import unittest
from src.run_summarization import make_soup, load_documents_for_topics, get_output_filename
from src.helpers.class_document import Document


class IOTests(unittest.TestCase):
    """
    Tests for file IO operations
    """

    def test_get_documents_for_topics(self):
        topic_soup = make_soup('test_topics.xml')
        topics = load_documents_for_topics(topic_soup)
        expected_topics = {'D0901A': [Document('XIN_ENG_20041113.0001'), Document('APW_ENG_20041118.0081')],
                           'D0902A': [Document('APW_ENG_20041011.0452'), Document('APW_ENG_20041017.0142')]}
        self.assertCountEqual(topics, expected_topics)

    def test_get_output_filename(self):
        topic_id = 'D0901A'
        output_file = get_output_filename(topic_id, 'test')

        self.assertEqual(output_file, '../outputs/D2/D0901-A.M.100.A.test')


if __name__ == '__main__':
    unittest.main()
