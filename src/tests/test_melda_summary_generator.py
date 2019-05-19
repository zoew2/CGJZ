import unittest
from src.run_summarization import parse_args
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.melda.melda_summary_generator import MeldaSummaryGenerator
from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors
from src.helpers.class_preprocessor import Preprocessor


class MeldaSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for MeldaSummaryGenerator
    """

    # variables used in multiple tests
    Preprocessor.load_models()
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_2 = Document("TST_ENG_20190101.0002")
    doc_list = [doc_1, doc_2]

    # topics = {'PUP1A': [doc_1, doc_2]}
    # w_map = {'he': 0, 'owners': 1, 'i': 2, 'played': 3, 'bigger': 4,
    #          'chased': 5, 'fetch': 6, 'park': 7, 'dog': 8, 'fun': 9,
    #          'toys': 10, 'tongues': 11, 'took': 12, 'ran': 13,
    #          'in': 14, 'sun': 15, 'loves': 16, 'somewhere': 17,
    #          'many': 18, 'together': 19, 'around': 20, 'puppy': 21,
    #          'today': 22, 'loads': 23, 'fight': 24, 'small': 25,
    #          "n't": 26, 'love': 27, 'wagging': 28, 'hanging': 29,
    #          'puppies': 30, 'bunch': 31, 'dogs': 32, 'get': 33,
    #          'playing': 34, 'they': 35, 'liked': 36, 'tails': 37,
    #          'run': 38, 'there': 39}

    args = parse_args(['test_data/test_topics.xml', 'test'])
    args.lda_topics = 4

    topics = {'PUP1A': [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002'),
                        Document('TST20190201.0001'), Document('TST20190201.0002')],
              'WAR2A': [Document('TST_ENG_20190301.0001'), Document('TST_ENG_20190301.0002'),
                        Document('TST20190401.0001'), Document('TST20190401.0002')]}
    WordMap.create_mapping()
    vec = Vectors()
    vec.create_freq_vectors(topics)
    idf = MeldaSummaryGenerator(doc_list, MeldaContentSelector(), args).get_idf_array()
    # summarizer = MeldaSummaryGenerator(doc_list, MeldaContentSelector(), args)


    def test_melda_info_ordering(self):
        summarizer = MeldaSummaryGenerator(self.topics['PUP1A'], MeldaContentSelector(), self.args)
        for doc in self.topics['PUP1A']:
            print(doc.vectors)
        content_selector = summarizer.select_content(self.idf)
        expected_len = len(content_selector)
        # lda_topics = self.args.lda_topics
        summarizer.order_information()

        actual_len = len(content_selector)

        self.assertEqual(expected_len, actual_len)

    def test_melda_generate_summary(self):

        for topic_id, documents in self.topics.items():
            summarizer = MeldaSummaryGenerator(documents, MeldaContentSelector(), self.args)
            summary = summarizer.generate_summary(self.idf)
            self.assertIsNot(summary, None)

if __name__ == '__main__':
    unittest.main()