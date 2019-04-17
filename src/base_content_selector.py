

class BaseContentSelector:
    """
    Functions to summarize documents
    """

    def select_content(self, documents):
        """
        Select the salient content for the summary
        (lead sentence of each document, ordered by date - least to most recent)
        :param: list of Document objects
        :return: list of Sentence objects
        """
        pass
