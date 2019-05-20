from src.base_files.base_content_selector import BaseContentSelector
from src.helpers.class_vectors import Vectors
from src.helpers.class_wordmap import WordMap
from scipy.spatial.distance import cosine
from scipy.sparse import csr_matrix
import numpy as np
np.seterr(divide='ignore', invalid='ignore')


class MeadContentSelector(BaseContentSelector):
    """
    Select content using MEAD scores
    """

    def get_sentence_position(self, sentence, document_length):
        """
        Get the position score for this sentence
        :param sentence: the given sentence
        :param document_length: the number of sentences in the document
        :return: float
        """
        i = sentence.position()
        # original equation adds 1 to the numerator but our sentence numbering
        # is zero-based so +1 isn't necessary
        p_score = ((document_length - i) / document_length)
        return p_score

    def get_first_sentence_overlap(self, sentence, first_sentence):
        """
        get cosine similarity between first sen and current sen
        :param sentence: curr sentence object
        :param first_sentence: first sentence object
        :return:
        """
        return 1 - cosine(first_sentence.vector.toarray(), sentence.vector.toarray())

    def get_cluster_centroid(self, documents, idf_array, threshold_calc):
        """
        The centroid for the cluster is the vector for
        the pseudo-document for the cluster, cf. MEAD paper
        :param: documents, idf_array, threshold (optional)
        :return: numpy array
        """
        word_sentence_matrix = Vectors().get_topic_matrix(documents).toarray()
        total_words_in_cluster = word_sentence_matrix.sum(0)
        sentences_per_word = np.count_nonzero(word_sentence_matrix, axis=0)  # across the cluster
        average_count = np.divide(total_words_in_cluster, sentences_per_word + 1)

        if len(average_count) != len(idf_array):
            raise Exception("Cluster centroid arrays must be the same length")

        centroid_cluster = np.multiply(average_count, idf_array)

        if threshold_calc == 'min':
            threshold = self.min_mean_threshold(centroid_cluster)
        elif threshold_calc == 'mean':
            threshold = self.mean_threshold(centroid_cluster)
        elif threshold_calc == 'max':
            threshold = self.max_mean_threshold(centroid_cluster)
        else:
            threshold = 0

        centroid_cluster[centroid_cluster < threshold] = 0  # set all centroid word values below threshold to zero
        return centroid_cluster

    def min_mean_threshold(self, centroid_cluster):
        """
        version 3 of threshold calculation: halfway between cluster mean & min
        :param centroid_cluster:
        :return:
        """
        cluster_min = centroid_cluster.min()
        cluster_mean = centroid_cluster.mean()
        threshold = (cluster_min + cluster_mean) / 2
        return threshold

    def max_mean_threshold(self, centroid_cluster):
        """
        version 1 of threshold calculation: halfway between cluster mean & max
        :param centroid_cluster:
        :return:
        """
        cluster_max = centroid_cluster.max()
        cluster_mean = centroid_cluster.mean()
        threshold = (cluster_max + cluster_mean) / 2
        return threshold

    def mean_threshold(self, centroid_cluster):
        """
        version 2 of threshold calculation: cluster mean
        :param centroid_cluster:
        :return:
        """
        threshold = centroid_cluster.mean()
        return threshold

    def get_centroid_score(self, sentence, centroid):
        """
        Get the centroid score for this sentence
        :param: sentence, centroid
        :return: float
        """
        centroid_score = 0
        for word in sentence.tokens:
            id = WordMap.id_of(word)
            centroid_score += centroid[id] if id is not None else 0
        return centroid_score

    def apply_redundancy_penalty(self, selected_sentence):
        """
        Apply a redundancy penalty to all sentences based on the given selected sentence
        :param selected_sentence: the selected sentence
        :return: void
        """
        selected_vector = selected_sentence.vector

        for sentence in self.selected_content:
            overlap = csr_matrix.sum((selected_vector != 0).multiply(sentence.vector != 0))
            counts = selected_vector.sum() + sentence.vector.sum()
            sentence.mead_score = sentence.mead_score - (overlap/counts)

    def calculate_scores(self, documents, args=None, idf_array=None):

        sentences = []
        c_scores = []
        p_scores = []
        f_scores = []
        centroid = self.get_cluster_centroid(documents, idf_array, args.c_threshold)

        for doc in documents:
            document_length = len(doc.sens)
            first_sentence = doc.get_sen_bypos(0)

            for sentence in doc.sens:
                sentence.c_score = self.get_centroid_score(sentence, centroid)
                sentence.p_score = self.get_sentence_position(sentence, document_length)
                sentence.f_score = self.get_first_sentence_overlap(sentence, first_sentence)

                c_scores.append(sentence.c_score)
                p_scores.append(sentence.p_score)
                f_scores.append(sentence.f_score)

                sentences.append(sentence)

        max_c = max(c_scores)
        return sentences, max_c, max([p*max_c for p in p_scores]), max(f_scores)

    def calculate_mead_scores(self, documents, args, idf_array=None):

        sentences, max_c, max_p, max_f = self.calculate_scores(documents, args, idf_array)

        # normalize all of the scores
        for sentence in sentences:
            sentence.c_score = sentence.c_score / max_c
            sentence.p_score = (sentence.p_score * max_c) / max_p
            sentence.f_score = sentence.f_score / max_f

            # add up the scores adjusted with optional score weights (default weights of 1)
            score = (args.w_c * sentence.c_score) + (args.w_p * sentence.p_score) + (args.w_f * sentence.f_score)
            sentence.set_mead_score(score)  # assign score value to Sentence object

        return sentences

    def select_content(self, documents, args, idf_array=None):
        """
        Select the salient content for the summary
        :param: list of Document objects
        :return: dictionary of Date, Sentence object pairs
        """
        sentences = self.calculate_mead_scores(documents, args, idf_array)
        self.selected_content = sentences
        return self.selected_content

