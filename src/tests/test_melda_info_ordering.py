import unittest
from src.helpers.class_preprocessor import Preprocessor
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors
from src.melda.melda_info_ordering import MeldaInfoOrdering
from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence
from src.run_summarization import parse_args
import numpy as np

class MeldaInfoOrderingTests(unittest.TestCase):
    """
    Tests for MeldaInfoOrdering
    """
    Preprocessor.load_models()

    TOPIC_NUM = 4
    FIRST_TOPIC = 2

    s0 = Sentence("In a park somewhere, a bunch of puppies played fetch with their owners today.\n", 1)
    s0.lda_scores = [0.1,  0.1,  0.9,  0.01]
    s0.set_mead_score(0.9)
    s0.melda_scores = np.add(s0.lda_scores, s0.mead_score)
    s1 = Sentence("I took my small puppy to the dog park today.\n", 1)
    s1.lda_scores = [0.1,  0.7,  0.4,  0.9]
    s1.set_mead_score(0.2)
    s1.melda_scores = np.add(s1.lda_scores, s1.mead_score)
    s2 = Sentence("He loves playing so he liked to run around with the other dogs playing fetch.\n", 1)
    s2.lda_scores = [0.8, 0.01, 0.7, 0.01]
    s2.set_mead_score(0.25)
    s2.melda_scores = np.add(s2.lda_scores, s2.mead_score)
    s3 = Sentence("Puppies love playing fetch.\n", 1)
    s3.lda_scores = [0.9, 0.01, 0.3, 0.7]
    s3.set_mead_score(0.1)
    s3.melda_scores = np.add(s3.lda_scores, s3.mead_score)

    input_summary = [s0, s1, s2, s3]

    args = parse_args(['test_data/test_topics.xml', 'test'])
    args.lda_topics = TOPIC_NUM

    orderer = MeldaInfoOrdering(args, input_summary)
    selector = MeldaContentSelector()

    should_be_vectors = np.array([[0.1,  0.1,  0.9,  0.01],
                                      [0.1,  0.7,  0.4,  0.9],
                                      [0.8, 0.01, 0.7, 0.01],
                                      [0.9, 0.01, 0.3, 0.7]])

    def test_pick_first_topic_by_first_sentence(self):
        # NOTE: since LDA is non-deterministic, this test just checks to see that
        # a top topic in the expected range [0-4] is returned for the first
        # sentence of the document cluster

        doc1 = Document("TST_ENG_20190101.0001")
        doc2 = Document("TST_ENG_20190101.0002")
        doc3 = Document("TST20190201.0001")
        doc4 = Document("TST20190201.0002")
        docs = [doc1, doc2, doc3, doc4]
        WordMap.create_mapping()
        topics = {'PUPS': docs}
        Vectors().create_term_doc_freq(topics)

        sentences = []
        for doc in docs:
            sentences.extend(doc.sens)

        lda_model = self.selector.build_lda_model(docs, self.TOPIC_NUM)
        self.selector.calculate_lda_scores(sentences, lda_model)

        expected_top_topic_list = [0, 1, 2, 3]
        actual_top_topic = self.orderer.pick_first_topic(method='first_sentence', documents=docs)

        self.assertIn(actual_top_topic, expected_top_topic_list)

    def test_pick_first_topic_by_mead_score(self):
        self.orderer.selected_content = self.input_summary

        actual_top_topic = self.orderer.pick_first_topic()
        expected_top_topic = self.FIRST_TOPIC

        self.assertEqual(actual_top_topic, expected_top_topic)

    def test_fill_topic_array(self):
        expected_vectors = self.should_be_vectors
        self.orderer.fill_topic_array()
        actual_vectors = self.orderer.topic_vectors

        self.assertListEqual(list(expected_vectors[1]), list(actual_vectors[1]))

    def test_reorder_content(self):
        self.orderer.first_sentence = None
        self.orderer.topic_vectors = self.should_be_vectors
        self.orderer.idx2sentence = {0: self.s0, 1: self.s1, 2: self.s2, 3: self.s3}
        self.orderer.first_topic = self.FIRST_TOPIC
        self.orderer.reorder_content()

        actual_sent_out = self.orderer.ordered_sentences
        expected_sent_out = [self.s0, self.s2, self.s3, self.s1]

        self.assertEqual(expected_sent_out, actual_sent_out)


if __name__ == '__main__':
    unittest.main()