from .base_content_selector import BaseContentSelector


class BaseSummaryGenerator:
    """
    Functions to summarize documents
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

        self.content_selector.select_content(self.documents)
        return self.content_selector.selected_content

    def order_information(self):
        """
        Order the salient information for the summary
        :return:
        """

        return self.content_selector.selected_content

    def realize_content(self):
        """
        Determine the surface realization for the content
        default behavior is to just take the first n sentences while the total word count < 100
        :param ordered_info: list of Sentence objects
        :return: new line separated string of sentences
        """

        output_content = []
        token_total = 0
        done = False
        while not done:
            next_sent = self.get_next_sentence(output_content)
            next_sent_len = next_sent.word_count
            if token_total + next_sent_len < 100:
                output_content.append(next_sent.raw_sentence)
                token_total += next_sent_len
            else:
                done = True
        output_content = '\n'.join(output_content)  # one sentence per line
        return output_content

    def get_next_sentence(self, summary):
        content = self.content_selector.selected_content
        return content.pop()

    def generate_summary(self):
        """
        Generate the summary
        :return:
        """

        self.select_content()
        self.order_information()
        return self.realize_content()
