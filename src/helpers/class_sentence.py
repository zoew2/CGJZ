"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""

from nltk import tokenize
import string
from nltk.corpus import stopwords
import spacy

from src.helpers.class_wordmap import WordMap



class Sentence:

    def __init__(self, raw_sentence, sent_pos, doc_id=None):
        """
        initialize Sentence class with methods for plain/raw and tokenized sentence
        options, word count, position of sentence in document and document id
        :param raw_sentence:
        :param sent_pos:
        """
        self.raw_sentence = raw_sentence.strip('\n')  # raw input form of current sentence
        self.sent_pos = int(sent_pos)  # position of sentence in document
        self.doc_id = doc_id
        self.tokens = []
        self.vector = []  # placeholder

        if not self.tokens:
            self.__tokenize_sentence()

        # update global mapping of words to indices
        WordMap.add_words(self.tokens)  # make sure self.tokens is the right thing here

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

    def stemming_n_linking_name_entity(self):
        """
        first find all name entities
        then lemmatize all the words that are not in an name entity

        :return: new_toks, type: string, e.g, ['New York', 'is', 'looking', 'at', 'buying', 'U.K.', 'startup', 'for', '$1 billion']

        """
        nlp = spacy.load("en")
        sen = nlp(self.raw_sentence)  # process sen

        entity_ind = [-1] * len(sen)
        ind = 0

        for ent in sen.ents:
            for i in range(ent.start, ent.end):
                entity_ind[i] = ind
            ind += 1
        # [0, 0, -1, -1, -1, -1, 1, -1, -1, 2, 2, 2]

        new_toks = []
        ent_ind = 0  # pointer to entities
        for i in range(len(entity_ind)):
            if_ent = entity_ind[i]
            if if_ent >= 0:  # if token is in an entity, just add to the new_toks, if not add stemmed word
                if i == 0:
                    new_toks.append(sen.ents[0].text)
                    ent_ind += 1
                elif entity_ind[i - 1] < 0:
                    new_toks.append(sen.ents[ent_ind].text)
                    ent_ind += 1
            else:
                new_toks.append(sen[i].text)

        return new_toks

    def __tokenize_sentence(self):
        """
        tokenize sentence and remove sentence-level punctiation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """

        stop_words = stopwords.words('english')
        stop_words.extend(['edu'])  # if we want to add any new words to stopwords

        words = tokenize.word_tokenize(self.raw_sentence)  # No NER or Stemming
        # words = self.stemming_n_linking_name_entity()  # NER and Stemming

        self.tokens = [w for w in words if (w not in string.punctuation and w not in stop_words)]
        # Strip punctuation and stopwords from sentence tokens

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
