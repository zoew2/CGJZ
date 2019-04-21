from src.base_files.base_content_selector import BaseContentSelector


class MeadSummaryGenerator(BaseContentSelector):
    """
    Summarize documents using MEAD
    """

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

        # TODO: create vectors

        # TODO: get topics_per_word

        # put this inside a loop over all the topics
        return self.content_selector.select_content(self.documents)

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

