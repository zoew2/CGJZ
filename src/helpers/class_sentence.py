"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""

# from nltk import tokenize
import string
from nltk.corpus import stopwords
import spacy


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

        if not self.tokens:
            self.__tokenize_sentence()

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
        first lemmatize all the words, then join them back to a sen string,
        then check name entity, retokenize the sen string
        (potential problem: words got lemmatized and not get recoginzed as a name entity;
        go through the sen string 2 times)
        :return: word tokens
        """
        nlp = spacy.load("en")
        sen = nlp(self.raw_sentence)
        tempsen = ' '.join([token.lemma_ for token in sen])  # stemmed and joined again to test for name entity

        newsen = nlp(tempsen)
        with newsen.retokenize() as retokenizer:
            for ent in newsen.ents:
                retokenizer.merge(newsen[ent.start:ent.end])
        return [token.text for token in newsen]



    def __tokenize_sentence(self):
        """
        tokenize sentence and remove sentence-level punctiation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """

        stop_words = stopwords.words('english')
        stop_words.extend(['edu'])  # if we want to add any new words to stopwords

        # words = tokenize.word_tokenize(self.raw_sentence)

        words = self.stemming_n_linking_name_entity()
        self.tokens = [w for w in words if (w not in string.punctuation and w not in stop_words)]
        # Strip punctuation and stopwords from sentence tokens

    def __str__(self):
        """
        print sentence as readable string
        """
        return self.raw_sentence

    def __eq__(self, other):
        return self.raw_sentence == other.raw_sentence
