from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.melda.melda_info_ordering import MeldaInfoOrdering
import re
from nltk.tokenize.treebank import TreebankWordDetokenizer
import warnings

class MeldaSummaryGenerator(MeadSummaryGenerator):
    """
    Summarize documents using MELDA
    """

    def pre_process(self, documents):
        """
        Preprocess the documents by tokenizing, removing stop words etc
        :return:
        """

        return documents

    def select_content(self, idf=None):
        """
        Select the salient content for the summary
        :return: list of Sentence objects
        """
        self.content_selector.select_content(self.documents, self.args, idf)
        return self.content_selector.selected_content

    def get_next_sentence(self, last_sentence=""):
        """
        Use Base Summary Generator's get_next_sentence function
        :param last_sentence: the last sentence selected for the summary
        :return: next Sentence
        """
        return super(MeldaSummaryGenerator, self).get_next_sentence(last_sentence)

    def order_information(self):
        """
        Call MeldaInfoOrdering class to perform cohesion gradient adjustment
        :param:
        """
        self.content_selector.selected_content = \
            MeldaInfoOrdering(self.args, self.content_selector.selected_content
                              ).run_cohesion_gradient(self.documents)

    def compress_sentences(self):
        sentences = []
        for sentence in self.content_selector.selected_content:
            compressed = []
            ignore = []
            remove_punct = remove_that = False
            for token in sentence.processed:
                head_dep = token.head.dep_
                attributives = ['said', 'claimed', 'reported']
                children = [child for child in token.children]
                child_deps = [child.dep_ for child in children]
                head_head = token.head.head.text
                if token.i in ignore or not token.text.rstrip():
                    continue

                # remove all adverbs
                if token.pos_ is 'ADV':
                    remove_punct = True
                    continue

                # remove initial conj
                if token.pos_ is 'CCONJ' and token.i is 0:
                    remove_punct = True
                    continue

                # remove punctuation following removed adv or initial conj unless it's sentence final
                if remove_punct:
                    if token.is_punct and token.i < len(token.doc)-1:
                        continue
                    else:
                        remove_punct = False

                # remove attributive words
                if token.text in attributives:
                    prep_indicies = [t.i for pp in token.children for t in pp.subtree if pp.dep_ is 'prep']
                    ignore.extend(prep_indicies)
                    remove_that = True
                    continue

                # remove 'that' if it's the start of a relative clause after an attributive word
                if remove_that:
                    if token.dep_ is 'mark':
                        continue
                    else:
                        remove_that = False

                # remove appositives and parenthesized info
                if len(child_deps) > 2 and "punct appos punct" in " ".join(child_deps):
                    punct = [child.i for child in children if child.is_punct]
                    ignore.extend([i for i in range(punct[0], punct[-1] + 1)])

                # remove the subject of an attribution
                if head_head in attributives and head_dep is 'nsubj':
                    tree_indices = [t.i for t in token.head.subtree]
                    ignore.extend(tree_indices)
                    continue

                # warn if there are any missed appositives (to revisit later)
                if token.dep_ is 'appos':
                    warnings.warn("missed appositive: " + token.doc.text)
                compressed.append(token.text)

            # fix capitalization, detokenize and strip any weird beginnings
            compressed[0] = compressed[0].capitalize()
            new_sentence = TreebankWordDetokenizer().detokenize(compressed)
            sentence_text = self.strip_beginning(new_sentence)

            # set compressed sentence on sentence object
            sentence.compressed = sentence_text
            sentences.append(sentence)

        self.content_selector.selected_content = sentences

    def realize_content(self):
        self.compress_sentences()
        return super(MeldaSummaryGenerator, self).realize_content()

    def generate_summary(self, idf_array=None):
        """
        Generate the summary
        :return:
        """
        self.select_content(idf_array)
        self.order_information()
        return self.realize_content()

    def strip_beginning(self, raw_sentence):
        matches = re.finditer(r"^[A-Z].*(-{2})", raw_sentence)
        indicies = [m.end() for m in matches]
        new_start_idx = indicies[0] if indicies else -1
        return raw_sentence[new_start_idx+1:]