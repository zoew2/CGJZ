import unittest
from src.mead.mead_content_selector import MeadContentSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors


class MeadSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for LeadSummaryGenerator
    """

    # variables used in multiple tests
    doc_1 = Document("TST_ENG_20190101.0001")
    doc_2 = Document("TST_ENG_20190101.0002")
    doc_list = [doc_1, doc_2]
    topics = {'PUP1A': [doc_1, doc_2]}
    w_map = {'he': 0, 'owners': 1, 'i': 2, 'played': 3, 'bigger': 4,
             'chased': 5, 'fetch': 6, 'park': 7, 'dog': 8, 'fun': 9,
             'toys': 10, 'tongues': 11, 'took': 12, 'ran': 13,
             'in': 14, 'sun': 15, 'loves': 16, 'somewhere': 17,
             'many': 18, 'together': 19, 'around': 20, 'puppy': 21,
             'today': 22, 'loads': 23, 'fight': 24, 'small': 25,
             "n't": 26, 'love': 27, 'wagging': 28, 'hanging': 29,
             'puppies': 30, 'bunch': 31, 'dogs': 32, 'get': 33,
             'playing': 34, 'they': 35, 'liked': 36, 'tails': 37,
             'run': 38, 'there': 39}
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

    def test_order_information(self):
        """
        Test ordering Sentences by MEAD score
        :return:
        """
        doc_id_1 = 'TST_ENG_20190101.0001'
        sentence_1 = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        sentence_2 = 'They all ran around with their tails wagging ' \
                     'and their tongues hanging out having loads of fun in the sun.'
        sentence_3 = 'I took my small puppy to the dog park today.'
        expected_info = [Sentence(sentence_1, 1, doc_id_1),
                         Sentence(sentence_3, 3, doc_id_1),
                         Sentence(sentence_2, 2, doc_id_1)]


        WordMap.word_to_id = self.w_map
        Vectors().create_freq_vectors(self.topics)
        generator = MeadSummaryGenerator(self.doc_list, MeadContentSelector())
        generator.select_content(self.idf)
        generator.order_information()

        first_sentences = generator.content_selector.selected_content[:3]

        self.assertListEqual(expected_info, first_sentences)

    def test_realize_content(self):
        """
        Test applying redundancy penalty during realize_content
        :return:
        """
        expected_content = "There were many bigger puppies but he didn't get in a fight with any of them, " \
                           "they just played together with their toys and chased each other.\n" \
                           "Puppies love playing fetch.\n" \
                           "He loves playing so he liked to run around with the other dogs playing fetch.\n" \
                           "They all ran around with their tails wagging and their tongues hanging out having loads of fun in the sun.\n" \
                           "I took my small puppy to the dog park today.\n" \
                           "In a park somewhere, a bunch of puppies played fetch with their owners today."

        WordMap.word_to_id = self.w_map
        Vectors().create_freq_vectors(self.topics)

        generator = MeadSummaryGenerator(self.doc_list, MeadContentSelector())
        generator.select_content(self.idf)
        generator.order_information()
        generator.content_selector.selected_content = generator.content_selector.selected_content
        realized_content = generator.realize_content()
        self.assertEqual(expected_content, realized_content)

    def test_get_idf_array(self):
        words = ["i", "eat", "cake", "is", "delicious",
                           "puppies", "are", "cute", "cats", "furry"]
        doc_list = [Document("TST_ENG_20190101.0001"), Document("TST_ENG_20190101.0002")]
        # Must override WordMap dictionary for test
        WordMap.word_to_id = {'delicious': 0, 'eat': 1, 'furry': 2,
                              'puppies': 3, 'i': 4, 'cats': 5,
                              'are': 6, 'is': 7, 'cute': 8, 'cake': 9}

        idf = MeadSummaryGenerator(doc_list, MeadContentSelector()).get_idf_array()

        scores = []
        for word in words:
            curr_score = idf[WordMap.id_of(word)]
            scores.append("{:.5f}".format(curr_score))

        expected_scores = ['1.37302', '3.25479', '2.91900',
                           '0.48039', '4.03294', '3.55582',
                           '0.76366', '4.03294', '4.03294',
                           '4.03294']

        self.assertListEqual(scores, expected_scores, 5)

    def test_mead_summary_length(self):
        """
        Test length of summary is less than 100 words
        :return:
        """
        topics = {'PUP1A': [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002'),
                            Document('TST20190201.0001'), Document('TST20190201.0002')],
                  'WAR2A': [Document('TST_ENG_20190301.0001'), Document('TST_ENG_20190301.0002'),
                            Document('TST20190401.0001'), Document('TST20190401.0002')]}
        WordMap.create_mapping()
        vec = Vectors()
        vec.create_freq_vectors(topics)
        idf = MeadSummaryGenerator.get_idf_array(self)
        max_length = 100

        for topic_id, documents in topics.items():
            generator = MeadSummaryGenerator(documents, MeadContentSelector())
            generator.select_content(idf)
            generator.order_information()
            generator.content_selector.selected_content = generator.content_selector.selected_content
            realized_content = generator.realize_content()
            realized_content = [w for w in realized_content.split(" ") if not " "]
            content_length = len(realized_content)
            self.assertLessEqual(content_length, max_length)

    # def test_generate_summary(self):
    #     topics = {'PUP1A': [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002'),
    #                         Document('TST20190201.0001'), Document('TST20190201.0002')],
    #               'WAR2A': [Document('TST_ENG_20190301.0001'), Document('TST_ENG_20190301.0002'),
    #                         Document('TST20190401.0001'), Document('TST20190401.0002')]}
    #     WordMap.create_mapping()
    #     vec = Vectors()
    #     vec.create_freq_vectors(topics)
    #     idf = MeadSummaryGenerator.get_idf_array(self)
    #
    #     for topic_id, documents in topics.items():
    #         summarizer = MeadSummaryGenerator(documents, MeadContentSelector())
    #         print(summarizer.generate_summary(idf))

if __name__ == '__main__':
    unittest.main()
