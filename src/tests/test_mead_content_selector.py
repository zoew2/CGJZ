import unittest
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.helpers.class_sentence import WordMap
from src.helpers.class_vectors import Vectors
# from scipy.sparse import dok_matrix
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

class MeadContentSelectorTests(unittest.TestCase):
    """
    Tests for MeadContentSelector
    """

    def test_get_sentence_position(self):
        sentence_1 = Sentence("Today is Friday, October 8, the 281st day of 2004.", 0)
        sentence_2 = Sentence("Markets are overcrowded, traffic jam is heavy and the shops are jostling " \
                     "with shoppers in the capital city of Srinagar in the Indian-administered Kashmir " \
                     "as the holy Moslem festival of Eid approaches here.", 50)

        pos_score_1 = MeadContentSelector.get_sentence_position(MeadContentSelector, sentence_1, 100)
        pos_score_2 = MeadContentSelector.get_sentence_position(MeadContentSelector, sentence_2, 100)

        expected_score_1 = 1
        expected_score_2 = 50/100

        self.assertEqual(expected_score_1, pos_score_1)
        self.assertEqual(expected_score_2, pos_score_2)


    def test_get_cluster_centroid(self):

        doc_1 = Document("TST_ENG_20190101.0001")
        doc_2 = Document("TST_ENG_20190101.0002")
        doc_3 = Document("TST_ENG_20190301.0001")
        doc_4 = Document("TST_ENG_20190301.0002")
        doc_list = [doc_1, doc_2]

        topics = {'PUP1A': [doc_1, doc_2], 'WAR2A': [doc_3, doc_4]}

        words = ['a', 'a', 'a', 'a', 'a', 'all', 'also',
                 'and', 'and', 'and', 'and', 'and', 'and',
                 'any', 'are', 'are', 'are', 'are', 'around',
                 'around', 'before', 'bigger', 'bombs',
                 'both', 'bunch', 'but', 'but', 'can',
                 'chased', 'country', "didn't", 'dog',
                 'dogs', 'each', 'enemies', 'enemy',
                 'fetch', 'fetch', 'fetch', 'fight',
                 'fight', 'fight', 'fun', 'get', 'get',
                 'go', 'goes', 'guns', 'hanging', 'have',
                 'have', 'have', 'having', 'he', 'he',
                 'he', 'hurt', 'i', 'in', 'in', 'in',
                 'in', 'is', 'just', 'kill', 'killed',
                 'like', 'liked', 'loads', 'lots', 'lots',
                 'love', 'loves', 'many', 'my', 'of', 'of',
                 'of', 'of', 'of', 'other', 'other', 'our',
                 'our', 'out', 'owners', 'park', 'park',
                 'people', 'people', 'played', 'played',
                 'playing', 'playing', 'playing', 'puppies',
                 'puppies', 'puppies', 'puppy', 'ran', 'run',
                 'shoot', 'shoot', 'small', 'so', 'so',
                 'soldiers', 'soldiers', 'somewhere', 'sun',
                 'tails', 'tanks', 'tanks', 'that', 'the',
                 'the', 'the', 'the', 'the', 'their', 'their',
                 'their', 'their', 'them', 'themselves',
                 'there', 'there', 'there', 'they', 'they',
                 'they', 'they', 'they', 'they', 'they',
                 'things', 'to', 'to', 'to', 'to', 'to',
                 'to', 'to', 'to', 'to', 'to', 'today',
                 'today', 'together', 'tongues', 'took',
                 'toys', 'travel', 'travel', 'try', 'used',
                 'used', 'vehicle', 'wagging', 'war', 'war',
                 'wars', 'weapon', 'weapons', 'were', 'when',
                 'wherever', 'with', 'with', 'with', 'with', 'with']

        WordMap.add_words(words)
        print("1 done")
        WordMap.create_mapping()
        print("2 done")
        Vectors().create_freq_vectors(topics)
        print("3 done")

        # m = doc_1.vectors
        #
        # print("vectors", m, type(m))
        idf = MeadSummaryGenerator().get_idf_array()
        print("4 done")

        # centroid = Vectors().get_topic_matrix(doc_list)

        centroid = MeadContentSelector().get_cluster_centroid(doc_list, idf)

        print(centroid)





if __name__ == '__main__':
    unittest.main()
