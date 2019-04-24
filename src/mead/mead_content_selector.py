from src.base_files.base_content_selector import BaseContentSelector
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cosine


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
            vector_ = (selected_vector != 0)
            overlap = csr_matrix.sum(vector_.multiply(sentence.vector != 0))
            counts = selected_vector.sum() + sentence.vector.sum()
            sentence.mead_score = sentence.mead_score - (overlap/counts)

    def get_score(self, sentence):
        """
        Get the MEAD score for this sentence
        :param sentence:
        :return:
        """
        pass
