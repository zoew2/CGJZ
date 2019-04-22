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
        return self.content_selector.selected_content.sort()

    def get_next_sentence(self, summary):
        self.content_selector.apply_redundancy_penalty(summary[-1])
        self.order_information()
        content = self.content_selector.selected_content
        return content.pop()
