from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_preprocessor import Preprocessor
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
import unittest

class MeldaContentSelectorTests(unittest.TestCase):
    preprocessor = Preprocessor()
    Preprocessor.init()
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_3 = Document("TST_ENG_20190301.0001")
    doc_list = [doc_1, doc_3]
    topics = {'PUPWAR': [doc_1, doc_3]}
    WordMap.create_mapping()
    WordMap.get_mapping()

    vec = Vectors()
    # vec.create_freq_vectors(topics)
    Vectors().create_term_doc_freq(topics)
    testtok = ['puppy', 'love', 'playing', 'fetch']
    testsen = Vectors().create_term_sen_freq(testtok)


    def test_LDA_model_and_score(self):


        generator = MeldaContentSelector(self.doc_list, MeldaContentSelector(), args=None)
        # generator.doLDA()
        print(generator.lda_model.print_topics())
        expected_topics=[]
        self.assertListEqual(expected_topics,generator.lda_model.print_topics())


        print(generator.lda_model.get_document_topics(self.testsen))
        expected_results=[]
        self.assertListEqual(expected_results, generator.lda_model.get_document_topics(self.testsen))


if __name__ == '__main__':
    unittest.main()
