"""
New MELDA class to handle information ordering of selected output
Uses a cohesion gradient for sentence topics
"""

from src.helpers.class_sentence import Sentence
from src.helpers.class_document import Document
from src.melda.melda_content_selector import MeldaContentSelector
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
        :param:
        """
        first_sent_topics = dd(int)

        for doc in documents:
            sentence = doc.get_sen_bypos(0)
            topics = MeldaContentSelector.get_LDA_score_of_sen(sentence)
            just_topics = [s for (t, s) in topics]
            max_topic = np.argmax(just_topics)
            first_sent_topics[max_topic] += 1

        self.first_topic = max(first_sent_topics, key=first_sent_topics.get)

    def fill_topic_array(self):
        """
        make a numpy array of sentences by number of topics
        :param:
        """
        self.topic_vectors = np.zeros(len(self.selected_content), self.num_topics)

        for index, sentence in enumerate(self.selected_content):
            # Fill array with topic values for each topic & make lookup dictionaries
            self.idx2sentence[index] = sentence
            sentence_lda = MeldaContentSelector.get_LDA_score_of_sen(sentence)
            sentence_lda_scores = [s for (t, s) in sentence_lda]
            self.topic_vectors[index] = sentence_lda_scores

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
        :param:
        """
        self.pick_first_topic(documents)
        self.fill_topic_array()
        self.reorder_content()
        return self.ordered_sentences
