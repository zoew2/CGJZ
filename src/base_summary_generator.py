from base_content_selector import BaseContentSelector


class BaseSummaryGenerator:
    """
    Functions to summarize documents
    Current implementation produces a summary consisting of the first sentence of each input document ordered by date
    (reverse chron)
    """

    def __init__(self, documents, content_selector):
        """
        Initialize this class by saving input documents
        :param documents: list of Document objects
        """
        self.documents = self.pre_process(documents)
        self.content_selector = content_selector or BaseContentSelector()

    def pre_process(self, documents):
        """
        Preprocess the documents by tokenizing, removing stop words etc
        :return:
        """

        return documents

    def select_content(self):
        """
        Select the salient content for the summary
        :return: list of Sentence objects
        """

        return self.content_selector.select_content(self.documents)

    def order_information(self, salient_info):
        """
        Order the salient information for the summary
        :return:
        """

        return salient_info

    def realize_content(self, ordered_info):
        """
        Determine the surface realization for the content
        default behavior is to just take the first n sentences while the total word count < 100
        :param ordered_info: list of Sentence objects
        :return: new line separated string of sentences
        """

        output_content = []
        token_total = 0
        while ordered_info:
            next_sent = ordered_info.pop().curr_sentence
            next_sent_len = len(next_sent.split(' '))
            if token_total + next_sent_len < 100:
                output_content.append(next_sent)
                token_total += next_sent_len
            else:
                break
        output_content = '\n'.join(output_content)  # one sentence per line
        return output_content

    def generate_summary(self):
        """
        Generate the summary
        :return:
        """

        salient_info = self.select_content()
        ordered_info = self.order_information(salient_info)
        surface_content = self.realize_content(ordered_info)

        return surface_content
