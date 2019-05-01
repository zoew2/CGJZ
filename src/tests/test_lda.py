import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
import unittest

class VectorsTests(unittest.TestCase):
    topics = {1: [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002')]}
    WordMap.create_mapping()
    mapping = WordMap.get_mapping()
    topic_one = topics.get(1)  # list of Documents

    def test_create_freq_vectors(self):
        Vectors().create_freq_vectors(self.topics)
        for doc_list in self.topics.values():
            for doc in doc_list:
                # check that there's a vector for each sentence
                print(doc.vectors)

                doc_matrix_shape = doc.vectors.get_shape()
                expected_rows = 3





if __name__ == '__main__':
    unittest.main()