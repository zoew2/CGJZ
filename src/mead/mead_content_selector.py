from src.base_files.base_content_selector import BaseContentSelector
from src.helpers.class_document import Document
from src.helpers.class_sentence import Sentence


class MeadContentSelector(BaseContentSelector):
    """
    Select content using MEAD scores
    """

    def get_sentence_position(self, sentence):
        pass

    def get_first_sentence_overlap(self, sentence):
        pass

    def get_centroid_score(self, sentence):
        pass

    def apply_redundancy_score(self):
        pass

    def calc_num_lda_topics(self, documents):
        """
        calculate the number of topics to model with LDA
        :param documents: list of Documents
        :return: int
        """""

        # calculate the average sentence length over the set of topic documents
        total_words = 0
        total_sentences = 0
        for document in documents:
            total_sentences += len(document.sens)
            for sentence in document.sens:
                total_words += sentence.word_count()
        average_sent_length = total_words / total_sentences
        return 100 / average_sent_length  # number of average-length sentences that can fit in a max-100 word summary

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
