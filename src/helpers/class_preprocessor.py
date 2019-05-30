import spacy
import string
from nltk.corpus import stopwords
import numpy as np
from nltk import tokenize
import neuralcoref

class Preprocessor:
    """
    do all the preprocessing
    """

    spacynlp = None
    stop_words = None

    @staticmethod
    def load_models():
        Preprocessor.spacynlp = spacy.load("en")
        coref_module = neuralcoref.NeuralCoref(Preprocessor.spacynlp.vocab)
        Preprocessor.spacynlp.add_pipe(coref_module, name='neuralcoref', before='ner')
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

        # process sen
        sen = Preprocessor.spacynlp(raw_sentence.strip())

        entity_ind = [0] * len(sen)
        ind = 1

        for ent in sen.ents:
            for i in range(ent.start, ent.end):
                entity_ind[i] = ind
            ind += 1

        # [1, 1, 0, 0, 0, 2, 0, 0, 3, 3, 3] # index > 0 are NEs

        if np.prod(entity_ind) != 0:  # if every word is a NE, not a sentence.
            return None

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
    def test_sent_preprocessing(sent):
        return tokenize.word_tokenize(sent.strip())

    @staticmethod
    def segment_sens(text):
        '''
        segments text into sentences
        :param text: multi-sentence String
        :return: list of Strings (sentences)
        '''

        return tokenize.sent_tokenize(text)

    @staticmethod
    def coref_resolve(text):
        '''
        identifies all spans in doc_text that refer to the same entity and replaces each one with the main mention of
        that entity
        :param text: String (raw text of an input document)
        :return: String
        '''

        coref_text = Preprocessor.spacynlp(text)._.coref_resolved
        if not coref_text:
            raise Exception('no coref text')
        return coref_text
