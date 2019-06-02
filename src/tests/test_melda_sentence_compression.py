import unittest
from src.helpers.class_preprocessor import Preprocessor
from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_sentence import Sentence
from src.run_summarization import parse_args
from src.melda.melda_summary_generator import MeldaSummaryGenerator

class MeldaSentenceCompressionTests(unittest.TestCase):
    """
    Tests for MeldaInfoOrdering
    """
    Preprocessor.load_models()

    s0 = Sentence("In a park somewhere, a bunch of puppies played fetch with their owners today.", 1)
    s1 = Sentence("I took my small puppy to the dog park today.", 1)
    s2 = Sentence("He loves playing so he liked to run around with the other dogs playing fetch.", 1)
    s3 = Sentence("Puppies love playing fetch.", 1)

    input_summary = [s0, s1, s2, s3]

    args = parse_args(['test_data/test_topics.xml', 'test'])
    args.n = 1

    selector = MeldaContentSelector()
    generator = MeldaSummaryGenerator([], selector, args)

    def test_remove_adverbs(self):
        s = Sentence("Puppies love running quickly and playing loudly.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies love running and playing."
        self.assertEqual(expected, summary)

    def test_remove_initial_conj(self):
        s = Sentence("But, puppies are great.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are great."
        self.assertEqual(expected, summary)

    def test_remove_parens(self):
        s = Sentence("The puppy (aka Mr. Mayor) was the cutest.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "The puppy was the cutest."
        self.assertEqual(expected, summary)

    def test_remove_appositives(self):
        s = Sentence("Dennis, the cutest puppy in the park, ran towards the ball.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Dennis ran towards the ball."
        self.assertEqual(expected, summary)

    def test_remove_junk(self):
        s = Sentence("Seattle, WA --- Puppies are great.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are great."
        self.assertEqual(expected, summary)

    def test_remove_attributions(self):
        s = Sentence("Julia said that puppies are cute.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are cute."
        self.assertEqual(expected, summary)

    def test_remove_attribution_phrases(self):
        s = Sentence("Seattle State Bureau of Animal Rating said "
                     "in a press release that puppies are cute.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are cute."
        self.assertEqual(expected, summary)

    def test_remove_temporal_mod(self):
        s = Sentence("By 8 a.m. on Saturday the park was full of puppies.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "The park was full of puppies."
        self.assertEqual(expected, summary)

    def test_remove_mod_rel(self):
        s = Sentence("Joe said that by 8 a.m. on Saturday the park was full of puppies.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "The park was full of puppies."
        self.assertEqual(expected, summary)

    def test_bad(self):
        s = Sentence("Heilongjiang Provincial Bureau of Environmental Protection said in a press release that by 6 a.m. on Saturday, concentration of nitrobenzene monitored at Sujiatun upstream Sifangtai, one major water intake spot of Harbin, capital of northeast China's Heilongjiang Province, fell to 0.0793 mg per liter, but above the state safety standard of 0.017 mg per liter, but the density of benzene stood at 0.0011 mg per liter, which is within   the state safety benchmark.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Concentration of nitrobenzene monitored at Sujiatun upstream Sifangtai fell, " \
                   "but above the state safety standard, but the density of benzene stood, " \
                   "which is within the state safety benchmark."
        self.assertEqual(expected, summary)

    def test_norweigan_oil(self):
        s = Sentence("Norwegian oil group Statoil said on Monday that it was trying to seal off a gas leak on a platform in the North Sea where production had been suspended and most employees evacuated owing to the risk of an explosion.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "It was trying to seal off a gas leak on a platform in the North Sea " \
                   "where production had been suspended " \
                   "and most employees evacuated owing to the risk of an explosion."
        self.assertEqual(expected, summary)


if __name__ == '__main__':
    unittest.main()