from src.base_content_selector import BaseContentSelector


class LeadSentenceSelector(BaseContentSelector):
    """
    Functions to summarize documents
    """

    def select_content(self, documents):
        """
        Select the salient content for the summary
        (lead sentence of each document, ordered by date - least to most recent)
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """

        selected_content = {doc.date+doc.art_id: doc.get_sen_bypos(0) for doc in documents}

        return selected_content
