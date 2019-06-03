import spacy
import string
from nltk.corpus import stopwords
import re
import itertools
import nltk

class Preprocessor:
    """
    do all the preprocessing
    """

    spacynlp = None
    stop_words = None

    @staticmethod
    def load_models():
        Preprocessor.spacynlp = spacy.load("en")
        Preprocessor.stop_words = stopwords.words('english')
        Preprocessor.stop_words.extend(['edu'])  # if we want to add any new words to stopwords

    @staticmethod
    def get_processed_sentence(raw_sentence):
        """

        :param raw_sentence:
        :return: sentence as a spacy doc
        """
        # return raw_sentence
        return Preprocessor.spacynlp(raw_sentence)

    @staticmethod
    def get_processed_tokens(processed):
        """
        returns the tokens in a given sentence with various processing done: lowercased, punctuation-only tokens
        and stop words removed (and optionally, lemmatizing non-NEs)
        :param processed: spacy Doc object
        :return: List of Strings (empty if all tokens are punctuation, stopwords or, optionally, NEs)
        commented code is for lemmatizing non-NEs
        """

        entities = set(processed.ents)
        entity_tokens = set([token for ent in entities for token in ent])
        unprocessed = set(processed) - entity_tokens

        processed_tokens = []
        processed_tokens.extend([e.text for e in processed.ents])
        all_entities = True
        for w in unprocessed:
            w = w.lemma_.lower()
            if w == '-pron-' or not w.rstrip():
                continue

            if w not in string.punctuation and w not in Preprocessor.stop_words:
                all_entities = False
                processed_tokens.append(w)

        return [] if all_entities else processed_tokens

    @staticmethod
    def is_bad_sentence(raw_sentence):
        # bad_patterns = re.findall(r"(-{3,} | \n[^\n*]{3,} | \d{10,})", raw_sentence)
        # return bool(bad_patterns)

        dashes = re.findall(r"-{3,}", raw_sentence)
        newlines = re.findall(r"([^\n]*\n){3,}", raw_sentence)
        numbers = re.findall(r"([^\d]*\d){10,}", raw_sentence)
        return bool(dashes) or bool(newlines) or bool(numbers)

    @staticmethod
    def strip_beginning(raw_sentence):
        matches = re.finditer(r"^[A-Z].*(-{2}|_)", raw_sentence)
        indicies = [m.end() for m in matches]
        new_start_idx = indicies[0] if indicies else -1
        return raw_sentence[new_start_idx+1:]
