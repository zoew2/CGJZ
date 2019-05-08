import spacy
import string
from nltk.corpus import stopwords


class Preprocessor:
    """
    do all the preprocessing
    """

    def __init__(self):
        self.spacynlp = spacy.load("en")
        self.stop_words = stopwords.words('english')
        self.stop_words.extend(['edu'])  # if we want to add any new words to stopwords

    def sent_preprocessing(self, raw_sentence):
        """
        first find all name entities
        then lemmatize all the words that are not in an name entity

        # :return: new_toks, type: string, e.g, ['New York', 'is', 'looking', 'at', 'buying', 'U.K.', 'startup', 'for', '$1 billion']
        :return: new_toks, type: list of string,
                            e.g, ['New York', 'is', 'looking', 'buying', 'U.K.', 'startup', '$1 billion']

        """

        sen = self.spacynlp(raw_sentence)  # process sen

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
                w = sen[i].text
                if w not in string.punctuation and w not in self.stop_words:  # Strip punctuation and stopwords from sentence tokens

                    new_toks.append(w)

        return new_toks
