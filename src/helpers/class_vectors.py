import numpy as np
from numpy import zeros
from scipy.sparse import dok_matrix, hstack, csc_matrix
from scr.helpers.class_wordmap import WordMap

class Vectors:
    """
    functions for making vector representations of sentences
    """

    map = WordMap()
    num_unique_words = len(map.get_mapping)

    def get_topics_per_word(self, topics):
        """
        :param topics: Dictionary (key: topic, value: list of Documents}
        for idf calculation
        :return: numpy array (total number of topics in which word corresponding to index appears)
        """
        # pre: create_freq_vectors has been called

        global num_unique_words
        totals = np.zeros((num_unique_words,), dtype=int)

        for doc_list in topics.values():
            topic_vectors = get_topic_matrix(doc_list)
            topic_vectors_csc = csc_matrix(topic_vectors)  # is this conversion helpful?? (csc efficient for col access)
            col_totals = topic_vectors_csc.sum(0)  # col_totals is the info needed for tf/count - way to store so it can be calculated only once?
            # Is there a to avoid looping over every word that appears in this topic?
            for index in col_totals.nonzero():
                totals[index] += 1
        return totals

    def get_topic_matrix(self, topic_docs):
        """
        returns a matrix of vectors representing all the sentences from all the documents with a topic
        :param topic_docs: list of Documents
        :return: dok_matrix (num sentences in topic X num words in corpus)
        """
        # pre: create_freq vectors has been called

        global num_unique_words
        topic_matrix = topic_docs[0].vectors  # initialize with vectors of first document in list
        index = 1
        # stack remaining document matrices
        while index < len(topic_docs):
            hstack(topic_matrix, topic_docs[index].vectors)
        return topic_matrix

    def create_binary_vectors(self, documents):
        """
        :param documents: list of Document objects
        :return:
        """
        # TODO
        pass

    def create_freq_vectors(self, topics):
        """
        creates a frequency vector for each sentence in each document in each topic in topics; stores single vectors in
        relevant Sentence objects and per-document matrices in relevant Document objects
        :param topics: Dictionary {topic -> list of Documents}
        :return: None
        """
        global num_unique_words
        for cluster in topics.values():
            for document in cluster:
                doc_vectors = dok_matrix((len(document.sens), num_unique_words))
                for sentence in document.sens:
                    sentence_vector = dok_matrix((1, num_unique_words))  # need default type here?
                    for word in sentence.tokens:  # change sent.tokens if doing NER/removing stopwords
                        word_id = mapping.id_of(word)
                        sentence_vector[0, word_id] += 1
                    # assign vector to sentence object
                    sentence.set_vector(sent_vector)
                    # add sentence vector to document matrix
                    hstack(doc_vectors, sentence_vector)
                # assign matrix to document
                document.set_vectors(doc_vectors)

