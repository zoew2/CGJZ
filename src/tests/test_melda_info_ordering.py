import unittest
from src.melda.melda_info_ordering import MeldaInfoOrdering
from src.helpers.class_document import Document
import numpy as np

class MeldaInfoOrderingTests(unittest.TestCase):
    """
    Tests for MeldaInfoOrdering
    """

    # variables used in multiple tests

    # todo: fix next two lines
    TOPIC_NUM = 4
    FIRST_TOPIC = 2
    FIRST_SUMMARY = ["In a park somewhere, a bunch of puppies played fetch with their owners today.\n",
                     "I took my small puppy to the dog park today.\n",
                     "He loves playing so he liked to run around with the other dogs playing fetch.\n",
                     "Puppies love playing fetch.\n"]

    orderer = MeldaInfoOrdering(TOPIC_NUM, FIRST_SUMMARY)

    orderer.idx2sentence = {0: "In a park somewhere, a bunch of puppies played fetch with their owners today.\n",
                           1: "I took my small puppy to the dog park today.\n",
                           2: "He loves playing so he liked to run around with the other dogs playing fetch.\n",
                           3: "Puppies love playing fetch.\n"}
                           # 4: "They all ran around with their tails wagging ",
                           # 5: "and their tongues hanging out having loads of fun in the sun.\n",
                           # 6: "There were many bigger puppies but he didn't get in a fight with any of them, "
                           # "they just played together with their toys and chased each other."
    orderer.first_topic = FIRST_TOPIC
    orderer.topic_vectors = np.array([[ 0.1,  0.1,  0.9,  0.01],
                                      [ 0.1,  0.7,  0.4,  0.9],
                                      [ 0.8, 0.01, 0.7, 0.01],
                                      [ 0.9, 0.01, 0.3, 0.7]])


    def test_pick_first_topic(self):
        docs = [Document("TST_ENG_20190101.0001"), Document("TST_ENG_20190101.0002"),
                Document("TST_ENG_20190102.0001"), Document("TST_ENG_20190102.0002")]

        expected_top_topic = self.FIRST_TOPIC
        actual_top_topic = self.orderer.pick_first_topic(docs)

        self.assertEqual(expected_top_topic, actual_top_topic)

    def test_fill_topic_array(self):
        expected_vectors = []
        self.orderer.fill_topic_array()
        actual_vectors = self.orderer.topic_vectors

        self.assertEqual(expected_vectors, actual_vectors)

    def test_reorder_content(self):

        expected_sent_out = ["In a park somewhere, a bunch of puppies played fetch with their owners today.\n",
                                 "He loves playing so he liked to run around with the other dogs playing fetch.\n",
                                 "Puppies love playing fetch.\n",
                                 "I took my small puppy to the dog park today.\n"]
        self.orderer.reorder_content()
        actual_sent_out = self.orderer.ordered_sentences

        self.assertEqual(expected_sent_out, actual_sent_out)


if __name__ == '__main__':
    unittest.main()