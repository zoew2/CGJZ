from src.mead.mead_summary_generator import MeadSummaryGenerator


class MeldaSummaryGenerator(MeadSummaryGenerator):
    """
    Summarize documents using MEAD
    """

    def __init__(self, documents, content_selector):
        """
        Initialize this class by saving input documents
        :param documents: list of Document objects
        """
        super().__init__(documents, content_selector)
        self.idf_array = None

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
        self.content_selector.select_content(self.documents, idf)
        return self.content_selector.selected_content

    def get_next_sentence(self, last_sentence=""):
        """
        Get the next Sentence from the selected content
        :param last_sentence: the last sentence selected for the summary
        :return: next Sentence
        """
        if last_sentence:
            self.content_selector.apply_redundancy_penalty(last_sentence)
            self.order_information()
        content = self.content_selector.selected_content
        return content.pop() if content else False

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()
