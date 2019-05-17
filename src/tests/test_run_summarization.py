import unittest
from src.run_summarization import make_soup, load_documents_for_topics, get_output_filename, parse_args
from src.helpers.class_document import Document
from src.helpers.class_preprocessor import Preprocessor
<<<<<<< HEAD

=======
>>>>>>> coref resolution and tests

class IOTests(unittest.TestCase):
    """
    Tests for file IO operations
    """

<<<<<<< HEAD
    Preprocessor.load_models()
=======
    Preprocessor.init()
>>>>>>> coref resolution and tests

    def test_get_documents_for_topics(self):
        topic_soup = make_soup('test_data/test_topics.xml')
        expected_topics = {'PUP1A': [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002'),
                                     Document('TST20190201.0001'), Document('TST20190201.0002')],
                           'WAR2A': [Document('TST_ENG_20190301.0001'), Document('TST_ENG_20190301.0002'),
                                     Document('TST20190401.0001'), Document('TST20190401.0002')]}
        topics = load_documents_for_topics(topic_soup)
        self.assertCountEqual(topics, expected_topics)

    def test_get_output_filename(self):
        topic_id = 'PUP1A'
        args = parse_args(['test_data/test_topics.xml', 'test', '--output_dir', '../outputs/D0/'])
        output_file = get_output_filename(topic_id, args)

        self.assertEqual(output_file, '../outputs/D0/PUP1-A.M.100.A.test-B-max-111')

    def test_argparse(self):
        args = parse_args(['test_data/test_topics.xml', 'test'])

        self.assertEqual(len(args._get_kwargs()), 10)


if __name__ == '__main__':
    unittest.main()
