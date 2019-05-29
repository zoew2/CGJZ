from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.base_files.base_summary_generator import BaseSummaryGenerator
from src.melda.melda_info_ordering import MeldaInfoOrdering
import re

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
            if_sen_valid = self.ifvalid_sent_reg(raw_sen)
            if if_sen_valid:
                processed_content.append(next_sent)
            next_sent = self.get_next_sentence(next_sent)
        return processed_content

    def ifvalid_sent_reg(self, raw_sen):
        pattern1 = re.compile("([\-])\\1\\1")
        pattern2 = re.compile(".*\n.*\n.*\n")
        pattern3 = re.compile(".*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d")

        return not (pattern1.match(raw_sen) or pattern2.match(raw_sen) or pattern3.match(raw_sen))

    def strip_beginning(self,raw_sen):
        toks = raw_sen.split()
        if toks[0].isupper():
            for ind,t in enumerate(toks):
                 if t == "--" or t == '_':
                    return ' '.join(toks[ind+1:])
        return raw_sen