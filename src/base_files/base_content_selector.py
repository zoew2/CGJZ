

class BaseContentSelector:
    """
    Functions to summarize documents
    """

    selected_content = None

    def select_content(self, documents, idf=None):
        """
        Select the salient content for the summary
        default functionality is just to return all sentences
        :param: list of Document objects
        :return: list of Sentence objects
        """
        sentences = [doc.sens for doc in documents]
        self.selected_content = [val for sublist in sentences for val in sublist]
