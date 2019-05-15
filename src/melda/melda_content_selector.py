from src.mead.mead_content_selector import MeadContentSelector
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors

import gensim


class MeldaContentSelector(MeadContentSelector):
    """
    Select content using MEAD scores
    """

    def __init__(self, documents, idf_array=None):
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """

        self.documents=documents
        self.lda_model = None
        self.doLDA()


    def select_content(self, documents, idf_array=None):
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """
        self.selected_content = []

        return self.selected_content

    def doLDA(self):
        topic_tdf = []
        for doc in self.documents:

            topic_tdf.append(doc.tdf)

        lda_model = gensim.models.ldamodel.LdaModel(corpus=topic_tdf,
                                                    id2word=WordMap.get_id2word_mapping(),
                                                    num_topics=2,
                                                    random_state=0,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)

        self.lda_model = lda_model

    def get_LDA_score_of_sen(self, sen):
        """

        :param sen: tokenized sentence, e.g.,['puppy', 'playing', 'fetch']
        :return: LDA score of sentense per topic[(0, 0.01499077), (1, 0.98500925)]
        """

        sen_tdf = Vectors().create_term_sen_freq(sen)
        return self.lda_model.get_document_topics(sen_tdf)
