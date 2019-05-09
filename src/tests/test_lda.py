import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from src.helpers.class_document import Document
import unittest


def main():
    topics = {1: [Document('TST_ENG_20190101.0001'), Document('TST_ENG_20190101.0002')]}
    WordMap.create_mapping()

    # mapping = WordMap.get_mapping()
    # topic_one = topics.get(1)  # list of Documents

    topic_tdf = []

    # def create_freq_vectors(self):

    Vectors().create_term_doc_freq(topics)
    for doc_list in topics.values():
        for doc in doc_list:
            topic_tdf.append(doc.tdf)
            print(doc.tokenized_text)

    lda_model = gensim.models.ldamodel.LdaModel(corpus=topic_tdf,
                                                id2word=WordMap.get_id2word_mapping(),
                                                num_topics=2,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    print(lda_model.print_topics())
    testtok = ['puppy', 'love', 'playing', 'fetch']
    testsen = Vectors().create_term_sen_freq(testtok)
    print(testsen)
    print(lda_model.get_document_topics(testsen))
    # doc_lda = lda_model[topicdocs]

    # print('\nPerplexity: ', lda_model.log_perplexity(topic_tdf))
    # print(lda_model.get_document_topics())


if __name__ == '__main__':
    main()
