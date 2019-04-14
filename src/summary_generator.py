from .content_selector import ContentSelector


class SummaryGenerator:
    """
    Functions to summarize documents
    """

    def __init__(self, documents):
        """
        Initialize this class by saving input documents
        :param documents: the input documents
        """
        self.documents = self.pre_process(documents)

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

        selector = ContentSelector()

        return selector.select_content(self.documents)

    def order_information(self, salient_info):
        """
        Order the salient information for the summary
        :return:
        """

        return salient_info

    def realize_content(self, ordered_info):
        """
        Determine the surface realization for the content
        :param ordered_info:
        :return:
        """

        return ordered_info

    def generate_summary(self):
        """
        Generate the summary
        :return:
        """

        salient_info = self.select_content()
        ordered_info = self.order_information(salient_info)
        surface_content = self.realize_content(ordered_info)

        return surface_content
