"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""


from nltk import tokenize
import string
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors

class Sentence:

    def __init__(self, raw_sentence, sent_pos, doc_id=None):
        """
        initialize Sentence class with methods for plain/raw and tokenized sentence
        options, word count, position of sentence in document and document id
        :param raw_sentence:
        :param sent_pos:
        """
        self.raw_sentence = raw_sentence.strip('\n')  # raw input form of current sentence
        self.sent_pos = int(sent_pos)    # position of sentence in document
        self.doc_id = doc_id
        self.tokens = []
        self.vector

        if not self.tokens:
            self.__tokenize_sentence()

        # update global mapping of words to indices
        map = WordMap()
        map.add_words(self.tokens)  # may want to change this later to take post-processing tokens

    def is_first_sentence(self):
        """
        grab headline and content(text) of the document
        :return: Boolean
        """
        if self.sent_pos == 0:
            return True
        else:
            return False

    def position(self):
        """
        returns position of sentence in document as a number
        :return: integer
        """
        return self.sent_pos

    def tokenized(self):
        """
        returns words in sentence excluding punctuation
        :return: list of words in sentence
        """
        return self.tokens

    def word_count(self):
        """
        count number of words in sentence excluding punctuation
        :return: integer
        """
        return len(self.tokens)

    def document_id(self):
        """
        return document id associated with sentence
        :return: String of document id or None if not provided
        """
        return self.doc_id

    def __tokenize_sentence(self):
        """
        tokenize sentence and remove sentence-level punctiation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """
        words = tokenize.word_tokenize(self.raw_sentence)
        # Strip punctuation from sentence tokens
        self.tokens = [w for w in words if w not in string.punctuation]

    def set_vector(self, vector):
        """
        assign a vector representing the sentence to self.vector
        :param vector: one-dimensional scipy sparse matrix
        :return:
        """
        self.vector = vector

    def __str__(self):
        """
        print sentence as readable string
        """
        return self.raw_sentence

    def __eq__(self, other):
        return self.raw_sentence == other.raw_sentence
