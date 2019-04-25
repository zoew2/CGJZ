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

    def test_order_information(self):
        """
        Test ordering Sentences by MEAD score
        :return:
        """
        doc_id_1 = 'TST_ENG_20190101.0001'
        sentence_1 = 'In a park somewhere, a bunch of puppies played fetch with their owners today.'
        sentence_2 = 'They all ran around with their tails wagging ' \
                     'and their tongues hanging out having loads of fun in the sun.'
        sentence_3 = 'Puppies love playing fetch.'
        expected_info = [Sentence(sentence_1, 1, doc_id_1),
                         Sentence(sentence_3, 3, doc_id_1),
                         Sentence(sentence_2, 2, doc_id_1)]

        documents = [Document('TST_ENG_20190101.0001')]

        ## This is hardcoded until Julia's code is merged
        documents[0].sens[0].mead_score = 0.8
        documents[0].sens[0].order_by = -0.8
        documents[0].sens[1].mead_score = 0.2
        documents[0].sens[1].order_by = -0.2
        documents[0].sens[2].mead_score = 0.5
        documents[0].sens[2].order_by = -0.5

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()

        first_sentences = generator.content_selector.selected_content

        self.assertListEqual(expected_info, first_sentences)

    def test_realize_content(self):
        """
        Test applying redundancy penalty during realize_content
        :return:
        """
        expected_content = "Puppies are cute because many of them are small.\n" \
                           "I took my small puppy to the dog park today.\n" \
                           "They all ran around with their tails wagging and their tongues hanging out having loads " \
                           "of fun in the sun.\n" \
                           "Puppies love playing fetch.\n"\
                           "In a park somewhere, a bunch of puppies played fetch with their owners today."

        documents = [Document('TST_ENG_20190101.0001'),
                     Document('TST_ENG_20190101.0002'),
                     Document('TST20190201.0001'),
                     Document('TST20190201.0002')]

        ## This is hardcoded until Julia's code is merged
        documents[0].sens[0].mead_score = 0.8
        documents[0].sens[0].order_by = -0.8
        documents[0].sens[1].mead_score = 0.2
        documents[0].sens[1].order_by = -0.2
        documents[0].sens[2].mead_score = 0.5
        documents[0].sens[2].order_by = -0.5

        WordMap.create_mapping()
        vec = Vectors()
        vec.create_freq_vectors({"PUP1A": documents})

        generator = MeadSummaryGenerator(documents, MeadContentSelector())
        generator.select_content()
        generator.order_information()
        generator.content_selector.selected_content = generator.content_selector.selected_content[:5]
        realized_content = generator.realize_content()

        self.assertEqual(expected_content, realized_content)

    def test_get_idf_array(self):
        words = ["i", "eat", "cake", "is", "delicious",
                           "puppies", "are", "cute", "cats", "furry"]
        WordMap.add_words(words)
        WordMap.create_mapping()
        idf = MeadSummaryGenerator().get_idf_array()

        puppies_idf_score = idf[WordMap.id_of('puppies')]
        cake_idf_score = idf[WordMap.id_of('cake')]
        i_idf_score = idf[WordMap.id_of('i')]
        eat_idf_score = idf[WordMap.id_of('eat')]
        is_idf_score = idf[WordMap.id_of('is')]
        are_idf_score = idf[WordMap.id_of('are')]
        delicious_idf_score = idf[WordMap.id_of('delicious')]
        cute_idf_score = idf[WordMap.id_of('cute')]
        cats_idf_score = idf[WordMap.id_of('cats')]
        furry_idf_score = idf[WordMap.id_of('furry')]

        print(puppies_idf_score, cake_idf_score, i_idf_score, eat_idf_score, is_idf_score)

        puppies_expected = 3.5558196830611912
        cake_expected = 2.918997585474017
        i_expected = 1.3730247377110034
        eat_expected = 3.25478968739721
        is_expected = 0.48039438982519317
        are_expected = 0.763661548008955
        zero_expected = 4.032940937780854

        self.assertAlmostEqual(puppies_idf_score, puppies_expected, 5)
        self.assertAlmostEqual(cake_idf_score, cake_expected, 5)
        self.assertAlmostEqual(i_idf_score, i_expected, 5)
        self.assertAlmostEqual(eat_idf_score, eat_expected, 5)
        self.assertAlmostEqual(is_idf_score, is_expected, 5)
        self.assertAlmostEqual(are_idf_score, are_expected, 5)
        self.assertAlmostEqual(delicious_idf_score, zero_expected, 5)
        self.assertAlmostEqual(cute_idf_score, zero_expected, 5)
        self.assertAlmostEqual(cats_idf_score, zero_expected, 5)
        self.assertAlmostEqual(furry_idf_score, zero_expected, 5)


if __name__ == '__main__':
    unittest.main()
