from src.mead.mead_content_selector import MeadContentSelector


class MeldaContentSelector(MeadContentSelector):
    """
    Select content using MEAD scores
    """

    def select_content(self, documents, idf_array=None):
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """
        self.selected_content = []

        return self.selected_content

