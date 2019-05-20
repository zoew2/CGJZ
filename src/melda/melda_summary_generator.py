from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.base_files.base_summary_generator import BaseSummaryGenerator
from src.melda.melda_info_ordering import MeldaInfoOrdering

class MeldaSummaryGenerator(MeadSummaryGenerator):
    """
    Summarize documents using MEAD
    """

    def pre_process(self, documents):
        """
        Preprocess the documents by tokenizing, removing stop words etc
        :return:
        """

        return documents

    def select_content(self, idf=None):
        """
        Select the salient content for the summary
        :return: list of Sentence objects
        """
        self.content_selector.select_content(self.documents, self.args, idf)
        return self.content_selector.selected_content

    def get_next_sentence(self, last_sentence=""):
        """
        Use Base Summary Generator's get_next_sentence function
        :param last_sentence: the last sentence selected for the summary
        :return: next Sentence
        """
        return BaseSummaryGenerator(self.documents, self.content_selector,
                                    self.args).get_next_sentence(last_sentence)

    def order_information(self):
        """
        Call MeldaInfoOrdering class to perform cohesion gradient adjustment
        :param:
        """
        self.content_selector.selected_content = \
            MeldaInfoOrdering(self.args, self.content_selector.selected_content
                              ).run_cohesion_gradient(self.documents)

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()
