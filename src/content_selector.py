

class ContentSelector:
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
        chron_docs = sorted(documents, key=Document.date)  # most recent last
        selected_content = [doc.get_sen_bypos(0) for doc in chron_docs]

        return selected_content
