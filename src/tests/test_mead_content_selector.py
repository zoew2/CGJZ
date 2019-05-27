import unittest
from src.run_summarization import parse_args
from src.mead.mead_content_selector import MeadContentSelector
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.helpers.class_sentence import WordMap
from src.helpers.class_vectors import Vectors
from src.helpers.class_preprocessor import Preprocessor
import numpy as np

class MeadContentSelectorTests(unittest.TestCase):
    """
    Tests for MeadContentSelector
    """

    # variables used in multiple tests
    Preprocessor.load_models()
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_2 = Document("TST_ENG_20190101.0002")
    doc_list = [doc_1, doc_2]
    topics = {'PUP1A': [doc_1, doc_2]}
    w_set = {'he', 'owner', 'i', 'play', 'big',
             'chase', 'fetch', 'park', 'dog', 'fun',
             'toy', 'tongue', 'take', 'ran',
             'in', 'sun', 'love', 'somewhere',
             'many', 'together', 'around', 'puppy',
             'today', 'load', 'fight', 'small',
             "n't", '-PRON-', 'wag', 'hang',
             'loads', 'bunch', 'get', 'playing',
             'they', 'like', 'tail', 'run', 'there'}

    w_map = {'he':1, 'owner':2, 'i':3, 'play':4, 'big':5,
             'chase':6, 'fetch':7, 'park':8, 'dog':9, 'fun':10,
             'toy':11, 'tongue':12, 'take':13, 'ran':14,
             'in':15, 'sun':16, 'love':17, 'somewhere':18,
             'many':19, 'together':20, 'around':21, 'puppy':22,
             'today':23, 'load':24, 'fight':25, 'small':26,
             "n't":27, '-PRON-':28, 'wag':29, 'hang':30,
             'loads':31, 'bunch':32, 'get':33, 'playing':34,
             'they':35, 'like':36, 'tail':37, 'run':38, 'there':39}

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

    # idf = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    #        1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    #        1, 2, 3]

    args = parse_args(['test_data/test_topics.xml', 'test'])
    args.c_threshold = 'min'

    def test_get_sentence_position(self):
        selector = MeadContentSelector()
        sentence_1 = Sentence("Here is a test sentence.", 0)
        sentence_2 = Sentence("Here is another one.", 50)

        pos_score_1 = selector.get_sentence_position(sentence_1, 100)
        pos_score_2 = selector.get_sentence_position(sentence_2, 100)

        expected_score_1 = 1
        expected_score_2 = 50/100

        self.assertEqual(expected_score_1, pos_score_1)
        self.assertEqual(expected_score_2, pos_score_2)


    def test_get_cluster_centroid(self):
        selector = MeadContentSelector()
        WordMap.word_set = self.w_set
        WordMap.word_to_id = self.w_map
        Vectors().create_freq_vectors(self.topics)

        centroid = selector.get_cluster_centroid(self.doc_list, self.idf, self.args.c_threshold)

        actual_non_zero = np.count_nonzero(centroid)
        should_be_non_zero = 29

        self.assertEqual(actual_non_zero, should_be_non_zero)

    def test_get_centroid_score(self):
        selector = MeadContentSelector()
        sent_1 = Sentence("Puppies love playing fetch.", 0)
        self.args.c_threshold = 'mean'

        WordMap.word_set = self.w_set
        WordMap.word_to_id = self.w_map
        Vectors().create_freq_vectors(self.topics)

        centroid = selector.get_cluster_centroid(self.doc_list, self.idf, self.args.c_threshold)

        expected_centroid_score = 6.3
        c_score = selector.get_centroid_score(sent_1, centroid)

        self.assertAlmostEqual(expected_centroid_score, c_score, 1)

    def test_apply_redundancy_penalty(self):
        """
        Test the function to apply the redundancy penalty
        :return:
        """
        selector = MeadContentSelector()

        WordMap.word_set = self.w_set
        WordMap.create_mapping()
        Vectors().create_freq_vectors(self.topics)

        selected = selector.select_content(self.doc_list, self.args, self.idf)
        selector.apply_redundancy_penalty(selected[0])
        scores = [s.mead_score for s in selector.selected_content]
        expected_scores = [1.9003829413846463, 1.6243717975775935, 0.6522065176000799,
                           2.3571461578060453, 1.532600545620478, 1.7661796758000055]

        self.assertEqual(scores, expected_scores)

    def test_select_content(self):
        selector = MeadContentSelector()
        Vectors().create_freq_vectors(self.topics)
        selected = selector.select_content(self.topics['PUP1A'], self.args, self.idf)
        top_sentence = selected[0]
        expected_top_sentence = 'In a park somewhere, a bunch of ' \
                                'puppies played fetch with their owners today.'

        top_mead_score = float("{:.5f}".format(top_sentence.mead_score))
        expected_top_mead_score = 2.40038

        self.assertEqual(top_sentence.raw_sentence, expected_top_sentence)
        self.assertEqual(top_mead_score, expected_top_mead_score)


if __name__ == '__main__':
    unittest.main()
