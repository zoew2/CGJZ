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
    doc_3 = Document("TST_ENG_20190301.0001")
    doc_list = [doc_1, doc_3]
    topics = {'PUPWAR': doc_list}

    w_set = {'park', 'somewhere', 'bunch', 'puppy', 'play', 'fetch', 'their', 'owner', 'today', 'they', 'all', 'run',
             'around', 'their', 'tail', 'wag', 'tongue', 'hang', 'out', 'have', 'load', 'fun', 'sun', 'love', 'our',
             'country', 'go', 'war', 'soldier', 'go', 'fight', 'travel', 'wherever', 'fight', 'enemy', 'try', 'kill',
             'before', 'get', 'kill', 'themselves', '-PRON-', 'playing'}

    idf = [4.032940937780854, 2.420157081061118, 1.3730247377110034,
           2.8868129021026157, 2.7776684326775474, 3.7319109421168726,
           3.25478968739721, 2.7107216430469343, 3.7319109421168726,
           4.032940937780854, 3.3339709334448346, 4.032940937780854,
           1.9257309681329853, 2.5705429398818973, 0.21458305982249878,
           2.3608430798451363, 3.5558196830611912, 3.3339709334448346,
           1.5660733174267443, 2.024340766018936, 1.2476111027700865,
           4.032940937780854, 0.9959130580250786, 3.7319109421168726,
           2.5415792439465807, 1.7107216430469343, 4.032940937780854,
           3.4308809464528913, 4.032940937780854, 3.4308809464528913,
           3.5558196830611912, 3.5558196830611912, 4.032940937780854,
           1.734087861371147, 3.0786984283415286, 0.9055121599292547,
           3.5558196830611912, 3.5558196830611912, 1.9876179589941962]

    args = parse_args(['test_data/test_topics.xml', 'test'])
    args.lda_topics = 2

    def test_melda_info_ordering(self):
        WordMap.word_set = self.w_set
        WordMap.create_mapping()
        Vectors().create_freq_vectors(self.topics)
        Vectors().create_term_doc_freq(self.topics)
        summarizer = MeldaSummaryGenerator(self.doc_list, MeldaContentSelector(), self.args)
        content_selector = summarizer.select_content(self.idf)
        expected_len = len(content_selector)
        summarizer.order_information()

        actual_len = len(content_selector)

        self.assertEqual(expected_len, actual_len)

    def test_melda_generate_summary(self):
        WordMap.word_set = self.w_set
        WordMap.create_mapping()
        Vectors().create_freq_vectors(self.topics)
        Vectors().create_term_doc_freq(self.topics)
        for topic_id, documents in self.topics.items():
            summarizer = MeldaSummaryGenerator(documents, MeldaContentSelector(), self.args)
            summary = summarizer.generate_summary(self.idf)
            self.assertIsNot(summary, None)

    def test_ifvalid_sent(self):
        for topic_id, documents in self.topics.items():
            summarizer = MeldaSummaryGenerator(documents, MeldaContentSelector(), self.args)
            break
        raw_sent1="--"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent1),1)

        raw_sent2="---"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent2),0)

        raw_sent3="-342--"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent3),1)

        raw_sent4="-342dafd23480134"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent4),0)

        raw_sent5="\n\nsafadj\n\n"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent5),0)

        raw_sent6="-342dafd23480"
        self.assertEqual(summarizer.ifvalid_sent_reg(raw_sent6),1)


    def test_strip_beginning(self):
        for topic_id, documents in self.topics.items():
            summarizer = MeldaSummaryGenerator(documents, MeldaContentSelector(), self.args)
            break
        raw_sent1 = "SHENZHEN, December 26 (Xinhua) -- Hong Kong has cat."
        self.assertEqual(summarizer.strip_beginning(raw_sent1), "Hong Kong has cat.")


if __name__ == '__main__':
    unittest.main()