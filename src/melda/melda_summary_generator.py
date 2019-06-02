from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.melda.melda_info_ordering import MeldaInfoOrdering
from src.melda.melda_content_realizer import MeldaContentRealizer

class MeldaSummaryGenerator(MeadSummaryGenerator):
    """
    Summarize documents using MELDA
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
        return super(MeadSummaryGenerator, self).get_next_sentence(last_sentence)

    def order_information(self):
        """
        Call MeldaInfoOrdering class to perform cohesion gradient adjustment
        :param:
        """
        info_ordering = MeldaInfoOrdering(self.args, self.content_selector.selected_content)
        self.content_selector.selected_content = info_ordering.run_cohesion_gradient(self.documents)

    def realize_content(self):
        MeldaContentRealizer().compress_sentences(self.content_selector.selected_content)
        return super(MeldaSummaryGenerator, self).realize_content()

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()
