from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.base_files.base_summary_generator import BaseSummaryGenerator
from src.melda.melda_info_ordering import MeldaInfoOrdering

class MeldaSummaryGenerator(MeadSummaryGenerator):
    """
    Summarize documents using MELDA
    """

    def pre_process(self, documents):
        """
        Preprocess the documents by tokenizing, removing stop words etc
        :return:
        """

        return documents

    def select_content(self, idf=None):
        """
        Select the salient content for the summary
        :return: list of Sentence objects
        """
        self.content_selector.select_content(self.documents, self.args, idf)
        return self.content_selector.selected_content

    def get_next_sentence(self, last_sentence=""):
        """
        Use Base Summary Generator's get_next_sentence function
        :param last_sentence: the last sentence selected for the summary
        :return: next Sentence
        """
        return BaseSummaryGenerator(self.documents, self.content_selector,
                                    self.args).get_next_sentence(last_sentence)

    def order_information(self):
        """
        Call MeldaInfoOrdering class to perform cohesion gradient adjustment
        :param:
        """
        self.content_selector.selected_content = \
            MeldaInfoOrdering(self.args, self.content_selector.selected_content
                              ).run_cohesion_gradient(self.documents)

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()

    def process_selected_content(self, selected_content):
        processed_content = []
        next_sent = self.get_next_sentence()
        while next_sent:
            raw_sen = next_sent.raw_sentence
            processed_sen = self.ifvalid_sent(raw_sen)
            if processed_sen:
                processed_content.append(processed_sen)
            next_sent = self.get_next_sentence(next_sent)
        return processed_content

    def ifvalid_sent(self, raw_sen):
        ct_consec_dash = 0  # int
        ifprev_dash = 0  # bool
        ct_nl = 0
        ct_d = 0

        for ind, cha in enumerate(raw_sen):
            if cha == '-':
                if ind == 0:
                    ct_consec_dash += 1
                    ifprev_dash = 1
                else:
                    if ifprev_dash:
                        ct_consec_dash += 1
                    else:
                        ct_consec_dash = 1
                    ifprev_dash = 1

                if ct_consec_dash >= 3:
                    return None
            else:
                ct_consec_dash = 0

                if cha == '\n':
                    ct_nl += 1
                    if ct_nl > 3:
                        return None

                elif cha.isdigit():
                    ct_d += 1
                    if ct_d > 10:
                        return None

        return 1