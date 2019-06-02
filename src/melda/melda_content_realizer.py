"""

"""

import re
from nltk.tokenize.treebank import TreebankWordDetokenizer

class MeldaContentRealizer:
    """

    """

    ATTRIBUTIVES = ['said', 'claimed', 'reported']
    TEMPORAL_TYPES = ['TIME', 'DATE']

    def compress_sentences(self, selected_sentences):
        sentences = []
        for sentence in selected_sentences:
            print("sentence:", sentence.raw_sentence)
            print("mead:", sentence.mead_score)
            print("centroid:", sentence.c_score)
            print("first:", sentence.f_score)
            print("pos:", sentence.p_score)
            print("lda:", sentence.lda_scores)
            print("melda:", sentence.melda_scores)
            print("tokens:", sentence.tokens)
            print("spacy tokens:", [t.text for t in sentence.processed])
            compressed = self.compress_sentence(sentence)

            # fix capitalization, detokenize and strip any bad beginnings
            if not compressed:
                continue
            compressed[0] = compressed[0].capitalize()
            new_sentence = TreebankWordDetokenizer().detokenize(compressed)
            sentence_text = self.strip_beginning(new_sentence)

            # set compressed sentence on sentence object
            sentence.compressed = sentence_text
            sentences.append(sentence)

        return sentences

    def compress_sentence(self, sentence):
        compressed, ignore = [], []
        remove_punct = remove_that = False
        for token in sentence.processed:

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
                if token.is_punct and token.i < len(token.doc) - 1:
                    continue
                else:
                    remove_punct = False

            # remove attributive words
            should_remove, indicies = self.remove_attribution(token)
            if should_remove:
                ignore.extend(indicies)
                remove_that = True
                continue

            # remove 'that' if it's the start of a relative clause after an attributive word
            if remove_that:
                if token.dep_ is 'mark':
                    continue
                else:
                    remove_that = False

            # remove appositives and parenthesized info
            should_remove, indicies = self.remove_appositives(token)
            if should_remove:
                ignore.extend(indicies)
                remove_punct = True

            # remove the subject of an attribution
            should_remove, indicies = self.remove_attribution_subj(token)
            if should_remove:
                ignore.extend(indicies)
                continue

            # remove temporal modifiers
            should_remove, indicies = self.remove_temporal_modifiers(token)
            if should_remove:
                ignore.extend(indicies)
                continue

            if not compressed and token.is_punct:
                continue

            compressed.append(token.text)

        return compressed

    def remove_attribution(self, token):
        should_remove = token.text in self.ATTRIBUTIVES

        prep_indicies = [t.i for pp in token.children for t in pp.subtree if pp.dep_ is 'prep']

        if should_remove:
            pp = [t.text for pp in token.children for t in pp.subtree if pp.dep_ is 'prep']
            print("removing attribution and preps: " + token.text + " " + " ".join(pp))

        return should_remove, prep_indicies

    def remove_appositives(self, token):
        children = [child for child in token.children]
        child_deps = [child.dep_ for child in children]
        should_remove = len(child_deps) > 2 and 'appos' in child_deps

        appos_indicies = [t.i for c in children for t in c.subtree if c.dep_ == 'appos']

        if should_remove:
            appos = [t.text for c in children for t in c.subtree if c.dep_ == 'appos']
            print("removing appositive: " + " ".join(appos))

        return should_remove, appos_indicies

    def remove_attribution_subj(self, token):
        attributive_ancestors = [a for a in token.ancestors if a.text in self.ATTRIBUTIVES]
        attributive_children = [c for a in attributive_ancestors for c in a.children if c.dep_ is 'nsubj']
        attribution_subj = [t.text for c in attributive_children for t in c.subtree]
        should_remove = attribution_subj and token.text == attribution_subj[0]

        if should_remove:
            attrib_phrase = [t.text for c in attributive_children for t in c.subtree]
            print("removing attributor: " + " ".join(attrib_phrase))

        return should_remove, [t.i for c in attributive_children for t in c.subtree]

    def remove_temporal_modifiers(self, token):
        pp = [t for t in token.subtree]
        descendants = [c for c in token.children]
        descendants.extend([g for c in token.children for g in c.children])

        nummod = [c.dep_ for c in token.children if c.dep_ == 'nummod' and not c.is_alpha]
        has_temporal = set([t.ent_type_ for t in pp]) & set(self.TEMPORAL_TYPES) or nummod
        should_remove = token.dep_ == 'prep' and has_temporal

        if should_remove:
            print("removing temp mod: " + " ".join([t.text for t in pp]))

        return should_remove, [t.i for t in pp]

    def strip_beginning(self, raw_sentence):
        matches = re.finditer(r"^[A-Z].*(-{2}|_)", raw_sentence)
        indicies = [m.end() for m in matches]
        new_start_idx = indicies[0] if indicies else -1
        return raw_sentence[new_start_idx+1:]
