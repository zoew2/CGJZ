from src.base_content_selector import BaseContentSelector


class MeadContentSelector(BaseContentSelector):
    """
    Functions to summarize documents
    """

    def get_sentence_position(self, sentence):
        pass

    def get_first_sentence_overlap(self, sentence):
        pass

    def get_centroid_score(self, sentence):
        pass

    def apply_redundancy_score(self):
        pass

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
        (lead sentence of each document, ordered by date - least to most recent)
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """

        # documents sorted by score
        selected_content = documents

        return selected_content
