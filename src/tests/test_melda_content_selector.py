from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_preprocessor import Preprocessor
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
from src.run_summarization import parse_args
import unittest

class MeldaContentSelectorTests(unittest.TestCase):
    Preprocessor.load_models()
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_3 = Document("TST_ENG_20190301.0001")
    doc_list = [doc_1, doc_3]
    topics = {'PUPWAR': [doc_1, doc_3]}
    WordMap.create_mapping()

    vec = Vectors()
    # vec.create_freq_vectors(topics)
    Vectors().create_term_doc_freq(topics)
    testtok = ['puppy', 'soldier', 'war', 'fetch']
    testsen = Vectors().create_term_sen_freq(testtok)

    selector = MeldaContentSelector()
    num_topics = 2
    lda_model = selector.build_lda_model(doc_list, num_topics)
    args = parse_args(['test_data/test_topics.xml', 'test'])

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
           3.5558196830611912, 3.5558196830611912, 1.9876179589941962,
           1.077734400238912]

    def test_document_topics(self):
        document_topics = self.lda_model.get_document_topics(self.testsen, minimum_probability=0)
        topic_dist = [prob[1] for prob in document_topics]

        self.assertEqual(len(topic_dist), self.num_topics)
        self.assertAlmostEquals(sum(topic_dist), 1, 2)


    def test_term_topics(self):
        puppy_topics = self.lda_model.get_term_topics(WordMap.id_of('puppy'), minimum_probability=0)
        war_topics = self.lda_model.get_term_topics(WordMap.id_of('war'), minimum_probability=0)
        puppy_dist = [prob[1] for prob in puppy_topics]
        enemy_dist = [prob[1] for prob in war_topics]

        puppy_war = puppy_dist[0] > enemy_dist[0] and puppy_dist[1] < enemy_dist[1]
        war_puppy = puppy_dist[0] < enemy_dist[0] and puppy_dist[1] > enemy_dist[1]

        self.assertTrue(puppy_war or war_puppy)

    def test_get_lda_scores(self):

        sentence = self.doc_list[0].sens[0]
        self.selector.calculate_lda_scores([sentence], self.lda_model)
        lda_scores = sentence.lda_scores

        self.assertEqual(len(lda_scores), self.num_topics)
        self.assertAlmostEqual(sum(lda_scores), 1, 2)

    def test_get_melda_scores(self):
        sentence = self.doc_list[0].sens[0]
        sentences = self.selector.calculate_mead_scores(self.doc_list, self.args, self.idf)
        self.selector.calculate_lda_scores(sentences, self.lda_model)
        self.selector.calculate_melda_scores(sentences)
        melda_scores = sentence.melda_scores

        self.assertEqual(len(melda_scores), self.num_topics)

    def test_get_top_n(self):
        sentences = self.selector.calculate_mead_scores(self.doc_list, self.args, self.idf)
        sentences = self.selector.calculate_lda_scores(sentences, self.lda_model)
        self.selector.select_top_n(sentences, self.num_topics, 1)

        self.assertEqual(len(self.selector.selected_content), self.num_topics)


if __name__ == '__main__':
    unittest.main()
