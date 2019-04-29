import unittest
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document


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
                doc_matrix_shape = doc.vectors.get_shape()
                expected_rows = 3
                self.assertEqual(doc_matrix_shape[0], expected_rows)

    def test_sentence_vector(self):
        s = self.topics.get(1)[1].sens[1]  # s1 is a Sentence object
        # s text: 'He loves playing so he liked to run around with the other dogs playing fetch.'
        id_of_playing = WordMap.id_of('playing')
        self.assertEqual(s.vector.getcol(id_of_playing).sum(), 2)
        for word in s.tokens:
            id_of_word = WordMap.id_of(word)
            self.assertGreater(s.vector.getcol(id_of_word).sum(), 0)

    def test_get_topic_matrix(self):
        # make sure all sentences from all topic docs make it into the matrix
        topic_one_matrix = Vectors().get_topic_matrix(self.topic_one)
        expected_num_sentences = 6
        self.assertEqual(expected_num_sentences, topic_one_matrix.get_shape()[0])


if __name__ == '__main__':
    unittest.main()