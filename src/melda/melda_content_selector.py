from src.mead.mead_content_selector import MeadContentSelector
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors
# from src.run_summarization import parse_args
import numpy as np
import gensim


class MeldaContentSelector(MeadContentSelector):
    """
    Select content using MELDA scores
    """

    lda_model = None

    def select_top_n(self, sentences, topics, n):
        """
        Select the top n sentences from each topic
        :param sentences: the sentences to pull from
        :param topics: the number of topics
        :param n: the number to pull from each topic
        :return: void
        """
        self.selected_content = []
        for idx in range(0, topics):
            for s in sentences:
                s.order_by = s.melda_scores[idx]
            sentences.sort()
            for num in range(0, n):
                sentence = sentences.pop()
                self.selected_content.append(sentence)
                self.apply_redundancy_penalty(sentence)
                sentences = self.calculate_melda_scores(sentences)
                sentences.sort()

    def calculate_lda_scores(self, sentences, lda_model):
        """
        Calculate LDA scores for each of the given sentences
        :param sentences: the given set of sentences
        :param lda_model: the LDA model
        :return: list of sentences with lda_scores populated
        """
        for sentence in sentences:
            sen_tdf = Vectors().create_term_sen_freq(sentence.tokens)
            lda_scores = lda_model.get_document_topics(sen_tdf, minimum_probability=0)
            lda_arr = np.zeros(len(lda_scores))
            for topic_id, prob in lda_scores:
                lda_arr[topic_id] = prob

            sentence.lda_scores = lda_arr * sentence.word_count()

        return sentences

    def calculate_melda_scores(self, sentences):
        """
        Calculate MELDA scores for each of the given sentences
        :param sentences: the given sentences
        :return: list of sentences with melda_scores populated
        """
        for sentence in sentences:
            sentence.melda_scores = sentence.lda_scores + sentence.mead_score

        return sentences

    def select_content(self, documents, args, idf_array=None,):
        """
        Select content based on MELDA scores
        :param documents: the list of documents
        :param args: arguments
        :param idf_array: idf array
        :return: list of selected sentences
        """
        lda_model = self.build_lda_model(documents, args.lda_topics)
        sentences = self.calculate_mead_scores(documents, args, idf_array)
        sentences = self.calculate_lda_scores(sentences, lda_model)
        sentences = self.calculate_melda_scores(sentences)
        self.select_top_n(sentences, args.lda_topics, args.n)
        return self.selected_content

    def build_lda_model(self, documents, num_topics):
        """
        Build the LDA model
        :param documents: the list of documents
        :param num_topics: the number of topics to use
        :return: the LDA model
        """
        topic_tdf = []
        for doc in documents:
            topic_tdf.append(doc.tdf)

        lda_model = gensim.models.ldamodel.LdaModel(
            corpus=topic_tdf,
            id2word=WordMap.get_id2word_mapping(),
            num_topics=num_topics,
            random_state=0,
            update_every=1,
            chunksize=100,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )

        return lda_model
