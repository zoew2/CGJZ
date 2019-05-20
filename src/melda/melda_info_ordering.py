"""
New MELDA class to handle information ordering of selected output
Uses a cohesion gradient for sentence topics
"""

from collections import defaultdict as dd
import numpy as np

class MeldaInfoOrdering():
    """
    Implement LDA topic-based sentence ordering after sentences have been selected
    """

    def __init__(self, args, selected_content):
        self.selected_content = selected_content
        self.first_topic = None
        self.num_topics = args.lda_topics
        self.topic_vectors = None
        self.idx2sentence = {}
        self.ordered_sentences = []

    def pick_first_topic(self, documents):
        """
        find top topic for the first sentence of documents in this cluster
        :param documents: the document set for the current cluster
        :return: int of top topic among first sentences of document
        """
        first_sent_topics = dd(int)

        for doc in documents:
            sentence = doc.get_sen_bypos(0)
            topics = sentence.lda_scores
            max_topic = np.argmax(topics)
            first_sent_topics[max_topic] += 1

        self.first_topic = max(first_sent_topics, key=first_sent_topics.get)
        return self.first_topic

    def fill_topic_array(self):
        """
        make a numpy array of sentences by number of topics
        :param:
        """
        self.topic_vectors = np.zeros((len(self.selected_content), self.num_topics))

        # Fill array with topic values for each topic & make lookup dictionaries
        for index, sentence in enumerate(self.selected_content):
            self.idx2sentence[index] = sentence
            self.topic_vectors[index] = sentence.lda_scores

    def reorder_content(self):
        """
        Do the reordering of the sentences in selected content using
        the cohesion gradient method
        :param:
        """
        sentence_queue = list(self.idx2sentence.keys())
        # topic_set = set(self.first_topic)
        curr_topic = self.first_topic

        while sentence_queue:
            sent_index = np.argmax(self.topic_vectors, axis=0)[curr_topic]
            sentence = self.idx2sentence[sent_index]
            self.ordered_sentences.append(sentence)
            sentence_queue.remove(sent_index)
            this_sentence_max = np.argmax(self.topic_vectors[sent_index])

            if this_sentence_max != curr_topic:
                # topic_set.add(curr_topic) # todo: Do we need to check that the topic isn't already covered?
                curr_topic = this_sentence_max

            # Remove sentence vector from numpy array & replace with zeros so that
            # the same sentence doesn't get added to summary repeatedly
            self.topic_vectors[sent_index] = np.zeros(self.num_topics)

        # return self.ordered_sentences

    def run_cohesion_gradient(self, documents):
        """
        order the sentences in selected_content 1) by
        first sentence topic overlap, then 2) by adding sentences
        according to gradual changes over topics
        :param documents: list of documents to pass into pick_first_topic function
        :return: int of top topic among first sentences of document
        """
        self.pick_first_topic(documents)
        self.fill_topic_array()
        self.reorder_content()
        return self.ordered_sentences
