"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""

import string
from src.helpers.class_wordmap import WordMap
from src.helpers.class_preprocessor import Preprocessor

class Sentence:

    def __init__(self, raw_sentence, sent_pos, doc_id=None):
        """
        initialize Sentence class with methods for plain/raw and tokenized sentence
        options, word count, position of sentence in document and document id
        NOTE: self.raw_sentence now reflects coreference resolution done on the whole document
        :param raw_sentence:
        :param sent_pos:
        """
        self.raw_sentence = raw_sentence.strip('\n')  # raw input form of current sentence
        self.__tokenize_sentence()  # try tokenize first, if not a proper sentence just throw exception don't bother

        self.sent_pos = int(sent_pos)  # position of sentence in document
        self.doc_id = doc_id
        self.vector = []  # placeholder
        self.order_by = self.sent_pos
        self.c_score = self.p_score = self.f_score = self.mead_score = self.lda_scores = self.melda_scores = None



        # update global mapping of words to indices
        WordMap.add_words(self.tokens)  # (use the tokens that we want represented in the vectors)

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
        ct = 0
        for w in self.raw_sentence.split(" "):
            if w not in string.punctuation:
                ct += 1
        return ct

    def document_id(self):
        """
        return document id associated with sentence
        :return: String of document id or None if not provided
        """
        return self.doc_id

    def set_mead_score(self, score):
        """
        assign sentence score
        :return: float
        """
        self.mead_score = score
        self.order_by = self.mead_score

    def get_score(self):
        """
        return sentence score
        :return: float
        """
        return self.mead_score

    def __tokenize_sentence(self):
        """
        tokenize sentence and remove sentence-level punctuation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """

        # stop_words = stopwords.words('english')
        # stop_words.extend(['edu'])  # if we want to add any new words to stopwords

        # words = tokenize.word_tokenize(self.raw_sentence)  # No NER or Stemming
        # words = self.stemming_n_linking_name_entity()  # NER and Stemming
        # self.tokens = [w.lower() for w in words if (w not in string.punctuation and w not in stop_words)]
        # Strip punctuation and stopwords from sentence tokens

        self.tokens = Preprocessor.sent_preprocessing(self.raw_sentence)  # NER and Stemming and striping stopwords and punc

        if not self.tokens:
            raise ValueError('not a sentence: ' + self.raw_sentence)
            raise Exception('not a sentence: ' + self.raw_sentence)

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
        """
        One Sentence is equal to another if the raw sentences match
        :param other:
        :return:
        """
        return isinstance(other, Sentence) and self.raw_sentence == other.raw_sentence


    def __lt__(self, other):
        """
        Sentences are ordered by their sentence positions by default
        if a Sentence has a mead score, that is used
        :param other:
        :return:
        """
        return self.order_by < other.order_by
