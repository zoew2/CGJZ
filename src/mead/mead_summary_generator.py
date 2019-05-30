from src.base_files.base_summary_generator import BaseSummaryGenerator
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_preprocessor import Preprocessor
from nltk.corpus import brown, reuters
import numpy as np


class MeadSummaryGenerator(BaseSummaryGenerator):
    """
    Summarize documents using MEAD
    """

    def __init__(self, documents, content_selector, args):
        """
        Initialize this class by saving input documents
        :param documents: list of Document objects
        """
        super().__init__(documents, content_selector, args)
        self.idf_array = None

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

    def get_idf_array(self):
        """
        Use external corpus to get IDF scores
        for cluster centroid calculations
        :return: numpy array of idf values
        """
        corpus = brown
        if self.args.corpus == 'R':
            corpus = reuters
        num_words = Vectors().num_unique_words
        n = len(corpus.fileids())  # number of documents in corpus
        docs_word_matrix = np.zeros([n, num_words])
        for doc_idx, doc_id in enumerate(corpus.fileids()):
            sentences = list(corpus.sents(doc_id))
            words_in_doc = set()
            for s in sentences:
                s = ' '.join(s)
                proc_s = Preprocessor().sent_preprocessing(s)
                if proc_s:
                    words_in_doc = words_in_doc.union(proc_s)
            for word in words_in_doc:
                word_idx = WordMap.id_of(word)
                if word_idx:
                    docs_word_matrix[doc_idx, word_idx] = 1

        docs_per_word = np.sum(docs_word_matrix, axis=0)
        self.idf_array = np.log10(np.divide(n, docs_per_word + 1))  # add one to avoid divide by zero error
        np.save('../src/helpers/idf_basic_' + self.args.corpus + '.npy', self.idf_array)
        return self.idf_array

    def get_next_sentence(self, last_sentence=""):
        """
        Get the next Sentence from the selected content
        :param last_sentence: the last sentence selected for the summary
        :return: next Sentence
        """
        if last_sentence:
            self.content_selector.apply_redundancy_penalty(last_sentence)
            self.order_information()
        content = self.content_selector.selected_content
        return content.pop() if content else False

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()
