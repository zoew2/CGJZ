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
                pos = token.pos_
                dep = token.dep_
                head = token.head.text
                head_dep = token.head.dep_
                head_subtree = [t for t in token.head.subtree]
                subtree = [t for t in token.subtree]
                attributives = ['said', 'claimed', 'reported']
                attributive_ancestors = [a for a in token.ancestors if a.text in attributives]
                attributive_children = [c for a in attributive_ancestors for c in a.children if c.dep_ is 'nsubj']
                attribution_subj = [t.text for c in attributive_children for t in c.subtree]
                children = [child for child in token.children]
                cchildren = [g for c in children for g in c.children]
                child_deps = [child.dep_ for child in children]


                if token.i in ignore or not token.text.rstrip():
                    continue

                # remove all adverbs
                if token.dep_ is 'advmod':
                    print("removing adverb: " + token.text)
                    remove_punct = True
                    continue

                # remove initial conj
                if token.pos_ is 'CCONJ' and token.i is 0:
                    print("removing initial conj: " + token.text)
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
                    pp = [t.text for pp in token.children for t in pp.subtree if pp.dep_ is 'prep']
                    print("removing attribution and preps: " + token.text + " " + " ".join(pp))
                    remove_that = True
                    continue

                # remove 'that' if it's the start of a relative clause after an attributive word
                if remove_that:
                    if token.dep_ is 'mark':
                        continue
                    else:
                        remove_that = False

                # remove appositives and parenthesized info
                if len(child_deps) > 2 and 'appos' in child_deps:
                    appos = [t.text for c in children for t in c.subtree if c.dep_ == 'appos']
                    appos_indicies = [t.i for c in children for t in c.subtree if c.dep_ == 'appos']
                    ignore.extend(appos_indicies)
                    remove_punct = True
                    print("removing appositive: " + " ".join(appos))

                # remove the subject of an attribution
                if attribution_subj and token.text == attribution_subj[0]:
                    tree_indices = [t.i for c in attributive_children for t in c.subtree]
                    ignore.extend(tree_indices)
                    attrib_phrase = [t.text for c in attributive_children for t in c.subtree]
                    print("removing attributor: " + " ".join(attrib_phrase))
                    continue

                # remove temporal modifiers
                pp = [t for t in token.subtree]
                descendants = [c for c in token.children]
                descendants.extend([g for c in token.children for g in c.children])
                deps = [c.dep_ for c in descendants]
                pp_ent_types = [t.ent_type_ for t in pp]
                temporal_types = ['TIME', 'DATE']
                has_temporal = set(pp_ent_types) & set(temporal_types) or 'nummod' in deps
                if token.dep_ == 'prep' and has_temporal:
                    pp_indicies = [t.i for t in pp]
                    ignore.extend(pp_indicies)
                    print("removing temp mod: " + " ".join([t.text for t in pp]))
                    continue

                if not compressed and token.is_punct:
                    continue

                compressed.append(token.text)

            # fix capitalization, detokenize and strip any weird beginnings
            if not compressed:
                continue
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
        matches = re.finditer(r"^[A-Z].*(-{2}|_)", raw_sentence)
        indicies = [m.end() for m in matches]
        new_start_idx = indicies[0] if indicies else -1
        return raw_sentence[new_start_idx+1:]