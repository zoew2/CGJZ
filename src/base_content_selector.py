

class BaseContentSelector:
    """
    Functions to summarize documents
    """

    def select_content(self, documents):
        """
        Select the salient content for the summary
        default functionality is just to return all sentences
        :param: list of Document objects
        :return: list of Sentence objects
        """
        sentences = [doc.sens for doc in documents]
        return [val for sublist in sentences for val in sublist]
