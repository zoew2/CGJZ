from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_preprocessor import Preprocessor
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
import unittest
import re

class MeldaContentSelectorTests(unittest.TestCase):
    preprocessor = Preprocessor()
    Preprocessor.init()
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_3 = Document("TST_ENG_20190301.0001")
    doc_list = [doc_1, doc_3]
    topics = {'PUPWAR': [doc_1, doc_3]}
    WordMap.create_mapping()

    vec = Vectors()
    # vec.create_freq_vectors(topics)
    Vectors().create_term_doc_freq(topics)
    testtok = ['puppy', 'love', 'playing', 'fetch']
    testsen = Vectors().create_term_sen_freq(testtok)



    def test_LDA_model_and_score(self):

        generator = MeldaContentSelector(self.doc_list)


        topics=generator.lda_model.print_topics()

        sum=0
        for t in topics:
            probs=re.findall(r'\d+\.\d+', t[1])
            for p in probs:
                sum += float(p)

        sen_topic_prob=generator.lda_model.get_document_topics(self.testsen)


        # random state introduced, can't compare results
        # expected_topics = [(0,
        #                     '0.184*"-PRON-" + 0.060*"enemy" + 0.060*"fight" + 0.060*"kill" + 0.060*"go" \
        #                     + 0.060*"war" + 0.060*"soldier" + 0.036*"    " + 0.036*"get" + 0.036*"travel"'),
        #                    (1,
        #                     '0.107*"-PRON-" + 0.061*"puppy" + 0.061*"fetch" + 0.037*"somewhere" + 0.037*"load" \
        #                     + 0.037*"bunch" + 0.037*"wag" + 0.037*"around" + 0.037*"park" + 0.037*"sun"')]


        self.assertTrue(1.1509-sum < 0.5)
        if len(sen_topic_prob)<2:
            self.assertAlmostEqual(float(sen_topic_prob[0][1]),0.99,2)
        else:
            self.assertTrue(abs(float(sen_topic_prob[0][1]) - float(sen_topic_prob[1][1]) ) >0.7)




if __name__ == '__main__':
    unittest.main()
