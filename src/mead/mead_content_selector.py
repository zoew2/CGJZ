from src.base_files.base_content_selector import BaseContentSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence
from scipy.spatial.distance import cosine
import numpy as np


class MeadContentSelector(BaseContentSelector):
    """
    Select content using MEAD scores
    """

    def get_sentence_position(self, sentence):
        pass

    def get_first_sentence_overlap(self, sentence, first_sentence):
        """
        get cosine similarity between first sen and current sen
        :param sentence: curr sentence object
        :param first_sentence: first sentence object
        :return:
        """
        return 1 - cosine(first_sentence.vector, sentence.vector)

    def get_centroid_score(self, sentence):
        pass

    def apply_redundancy_penalty(self, selected_sentence):
        """
        Apply a redundancy penalty to all sentences based on the given selected sentence
        :param selected_sentence: the selected sentence
        :return: void
        """
        selected_vector = selected_sentence.vector

        for sentence in self.selected_content:
            overlap = np.sum((selected_vector != 0) & (sentence.vector != 0))
            counts = np.sum(selected_vector) + np.sum(sentence.vector)
            sentence.mead_score = sentence.mead_score - (overlap/counts)

    def get_score(self, sentence):
        """
        Get the MEAD score for this sentence
        :param sentence:
        :return:
        """
        pass

    def select_content(self, documents):
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """

        # documents sorted by score
        selected_content = documents

        return selected_content
