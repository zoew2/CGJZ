from src.mead.mead_summary_generator import MeadSummaryGenerator
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

    def order_information(self):
        # TODO: check that this is the right way to do this; why does base summ gen have a return
        # statement in it?
        # todo: also - get next sentence needs to happen before information ordering
        self.content_selector.selected_content = MeldaInfoOrdering.cohesion_gradient(self.documents,
                                            self.content_selector.selected_content, self.args)


    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()
