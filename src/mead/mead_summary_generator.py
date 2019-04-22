from src.base_files.base_content_selector import BaseContentSelector


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

    def select_content(self):
        """
        Select the salient content for the summary
        :return:
        """
        return self.content_selector.select_content(self.documents)