from src.base_files.base_content_selector import BaseContentSelector


class LeadSentenceSelector(BaseContentSelector):
    """
    Functions to summarize documents
    """

    def select_content(self, documents, args, idf_array=None,):
        """
        Select the salient content for the summary
        (lead sentence of each document, ordered by date - least to most recent)
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """
        selected_content = []
        for doc in documents:
            lead_sentence = doc.get_sen_bypos(0)
            lead_sentence.order_by = int(doc.date + doc.art_id)
            selected_content.append(lead_sentence)

        self.selected_content = selected_content
