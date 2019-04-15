"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""


from nltk import tokenize
import string


class Sentence():

    def __init__(self, curr_sentence, sent_pos, doc_id=None):
        """
        initialize Sentence class
        :param curr_sentence:
        :param sent_pos:
        """
        self.curr_sentence = curr_sentence  # raw input form of current sentence
        self.sent_pos = int(sent_pos)    # position of sentence in document
        self.doc_id = doc_id    # TODO: do we need to be able to access the doc id for sentences?
        self.tokens = []

        if not self.tokens:
            self.__tokenize_sentence()

    def is_first_sentence(self):
        """
        grab headline and content(text) of the document
        :return Boolean:
        """
        if self.sent_pos == 1:
            return True
        else:
            return False

    def position(self):
        """
        returns position of sentence in document as a number
        :return:
        """
        return self.sent_pos

    def tokenized(self):
        """
        returns words in sentence excluding punctuation
        :return:
        """
        return self.tokens

    def word_count(self):
        """
        count number of words in sentence excluding punctuation
        :return:
        """
        return len(self.tokens)

    def document_id(self):  # TODO: check and see if we need this
        """
        return document id associated with sentence
        :return:
        """
        return self.doc_id

    def plain(self):
        """
       return plain text sentence without tokenization or punctuation stripping
       :return:
       """
        return self.curr_sentence

    def __tokenize_sentence(self):
        """
        tokenize sentence and remove sentence-level punctiation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """
        words = tokenize.word_tokenize(self.curr_sentence)
        # Strip punctuation from sentence tokens
        self.tokens = [w for w in words if w not in string.punctuation]

    def __str__(self):
        """
        print sentence as readable string
        """
        return self.curr_sentence
