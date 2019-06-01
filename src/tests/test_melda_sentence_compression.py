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
        self.assertEqual(summary, expected)

    def test_remove_initial_conj(self):
        s = Sentence("But, puppies are great.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are great."
        self.assertEqual(summary, expected)

    def test_remove_parens(self):
        s = Sentence("The puppy (aka Mr. Mayor) was the cutest.", 1)
        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "The puppy was the cutest."
        self.assertEqual(summary, expected)

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
        self.assertEqual(summary, expected)

    def test_remove_attributions(self):
        s = Sentence("Seattle State Bureau of Animal Rating said "
                     "in a press release that puppies are cute.", 1)

        self.selector.selected_content = [s]
        self.generator.compress_sentences()
        summary = "\n".join([s.compressed for s in self.selector.selected_content])

        expected = "Puppies are cute."
        self.assertEqual(summary, expected)

if __name__ == '__main__':
    unittest.main()