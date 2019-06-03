import spacy
import string
from nltk.corpus import stopwords
import re
import itertools
import nltk
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
    def get_processed_sentence(raw_sentence):
        # return raw_sentence
        return Preprocessor.spacynlp(raw_sentence)

    @staticmethod
    def get_processed_tokens(sen):
        # entities = [e.text.lower().split() for e in processed.ents]
        # entities = list(itertools.chain.from_iterable(entities))
        # processed = nltk.tokenize.word_tokenize(processed)

        # processed_tokens = []
        # # processed_tokens.extend([e.text for e in processed.ents])
        # all_entities = True
        # for w in processed:
        #     # w = w.lemma_.lower()
        #     w = w.text.lower()
        #     # w = w.lower()
        #     if w == '-pron-' or not w.rstrip():
        #         continue
        #
        #     if w not in string.punctuation and w not in Preprocessor.stop_words: # and w not in entities:
        #         all_entities = False
        #         processed_tokens.append(w)
        #
        # return [] if all_entities else processed_tokens
        entity_ind = [0] * len(sen)
        ind = 1
        for ent in sen.ents:
            for i in range(ent.start, ent.end):
                entity_ind[i] = ind
            ind += 1

        # [1, 1, 0, 0, 0, 2, 0, 0, 3, 3, 3] # index > 0 are NEs

        if np.prod(entity_ind) != 0:  # if every word is a NE, not a sentence.
            return []

        # linking NE
        new_toks = []
        ent_ind = 0  # pointer to entities
        for i in range(len(entity_ind)):

            if_ent = entity_ind[i]
            if if_ent > 0:  # if token is in an entity, just add to the new_toks, if not add stemmed word
                if i == 0:
                    new_toks.append(sen.ents[0].text)
                    ent_ind += 1
                elif entity_ind[i - 1] == 0:  # the tok before is not in a NE
                    new_toks.append(sen.ents[ent_ind].text)
                    ent_ind += 1
                elif entity_ind[i - 1] < if_ent:  # another NE follow right after it
                    new_toks.append(sen.ents[ent_ind].text)
                    ent_ind += 1
            else:

                w = sen[i].lemma_
                if w != '-PRON-':  # if w is not a NE, lowercase it
                    w = w.lower()
                else:
                    # w = sen[i].text
                    continue
                if w not in string.punctuation and w not in Preprocessor.stop_words:  # Strip punctuation and stopwords from sentence tokens

                    new_toks.append(w)

        return new_toks


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
        matches = re.finditer(r"^[*A-Z].*(-{2}|_)", raw_sentence)
        indicies = [m.end() for m in matches]
        new_start_idx = indicies[0] if indicies else -1
        return raw_sentence[new_start_idx+1:]
