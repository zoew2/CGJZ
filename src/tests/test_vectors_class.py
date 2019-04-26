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
        expected_vec_length = len(self.mapping)
        for doc_list in self.topics.values():
            for doc in doc_list:
                # check that there's a vector for each sentence and all vectors are the same length
                doc_matrix_shape = doc.vectors.get_shape()
                expected_rows = len(doc.sens)
                self.assertEqual(doc_matrix_shape, (expected_rows, expected_vec_length))
        # spot-check a sentence vector
        s1 = self.topics.get(1)[0].sens[0]  # s1 is a Sentence object
        s1_text = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        self.assertEqual(s1.raw_sentence, s1_text)
        id_of_puppies = WordMap.id_of('puppies')
        self.assertEqual(s1.vector.getcol(id_of_puppies).sum(), 1)
        for word in s1.tokens:
            id_of_word = WordMap.id_of(word)
            self.assertGreater(s1.vector.getcol(id_of_word).sum(), 0)

    def test_get_topic_matrix(self):
        # make sure all sentences from topic make it into the matrix
        topic_one_matrix = Vectors().get_topic_matrix(self.topic_one)
        expected_num_sentences = 6
        self.assertEqual(expected_num_sentences, topic_one_matrix.get_shape()[0])


if __name__ == '__main__':
    unittest.main()