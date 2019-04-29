from src.base_files.base_summary_generator import BaseSummaryGenerator


class LeadSummaryGenerator(BaseSummaryGenerator):
    """
    Functions to summarize documents
    Current implementation produces a summary consisting of the first sentence of each input document ordered by date
    (reverse chron)
    """

    def order_information(self):
        """
        Order the salient information for the summary
        :return: list of Sentence objects
        """

        return self.content_selector.selected_content.sort()
