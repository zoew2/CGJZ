from src.base_files.base_summary_generator import BaseSummaryGenerator


class MeadSummaryGenerator(BaseSummaryGenerator):
    """
    Summarize documents using MEAD
    """

    def pre_process(self, documents):
        """
        Preprocess the documents by tokenizing, removing stop words etc
        :return:
        """

        return documents

    def order_information(self):
        """
        Order the Sentences in selected content by MEAD score
        :return:
        """
        return self.content_selector.selected_content.sort()

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
