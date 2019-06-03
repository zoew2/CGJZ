import spacy
import string
from nltk.corpus import stopwords
import numpy as np

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
    def sent_preprocessing(raw_sentence):
        """
        first rule out wierd sentences
        then find all name entities
        then lemmatize all the words that are not in an name entity
        then get rid of stopwords and punt
        :return: new_toks, type: list of string,
                            e.g, ['New York', 'be', 'looking', 'buy', 'U.K.', 'startup', '$1 billion']
                            ['-PRON-', 'take', '-PRON-', 'small', 'puppy', 'dog', 'park', 'today']
                None, if not a proper sentence
        """
        # rule out weird sentences
        # ct_dash = 0
        # ct_nl = 0
        # ct_d = 0
        #
        #
        # for cha in raw_sentence:x
        #     if cha == '-':
        #         ct_dash += 1
        #         if ct_dash > 3:
        #             return None
        #     elif cha == '\n':
        #         ct_nl += 1
        #         if ct_nl > 3:
        #             return None
        #     elif cha.isdigit():
        #         ct_d += 1
        #         if ct_d > 10:
        #             return None

        # process sen
        sen = Preprocessor.spacynlp(raw_sentence)

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
