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

    def get_topic_matrix(self, topic_docs):
        """
        returns a matrix of vectors representing all the sentences from all the documents with a topic
        :param topic_docs: list of Documents
        :return: dok_matrix (num sentences in topic X num words in corpus)
        pre: create_freq vectors has been called
        """

        global num_unique_words
        topic_matrix = topic_docs[0].vectors  # initialize with vectors of first document in list
        index = 1
        # stack remaining document matrices
        while index < len(topic_docs):
            hstack(topic_matrix, topic_docs[index].vectors)
        return topic_matrix

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
                    sentence_vector = dok_matrix((1, num_unique_words))
                    for word in sentence.tokens:
                        word_id = mapping.id_of(word)
                        sentence_vector[0, word_id] += 1
                    # assign vector to sentence object
                    sentence.set_vector(sent_vector)
                    # add sentence vector to document matrix
                    hstack(doc_vectors, sentence_vector)
                # assign matrix to document
                document.set_vectors(doc_vectors)

