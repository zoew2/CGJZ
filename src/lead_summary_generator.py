from .base_summary_generator import BaseSummaryGenerator


class LeadSummaryGenerator(BaseSummaryGenerator):
    """
    Functions to summarize documents
    Current implementation produces a summary consisting of the first sentence of each input document ordered by date
    (reverse chron)
    """

    def order_information(self, salient_info):
        """
        Order the salient information for the summary
        :return: list of Sentence objects
        """

        return [salient_info[date] for date in sorted(salient_info.keys())]

    def realize_content(self, ordered_info):
        """
        Determine the surface realization for the content
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
