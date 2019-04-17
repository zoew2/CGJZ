import unittest
from src.lead_sentence_selector import LeadSentenceSelector
from src.lead_summary_generator import LeadSummaryGenerator
from src.class_document import Document


class LeadSummaryGeneratorTests(unittest.TestCase):
    """
    Tests for LeadSummaryGenerator
    """

    def test_order_information(self):
        documents = [Document('XIN_ENG_20041113.0001'), Document('APW_ENG_20041011.0001')]
        expected_content = "Today is Friday, October 8, the 281st day of 2004.\n" \
                           "Describe the debate over use of emergency contraceptives, " \
                           "also called the morning-after pill, " \
                           "and whether or not it should be available without a prescription."

        generator = LeadSummaryGenerator(documents, LeadSentenceSelector())
        ordered_info = generator.select_content()
        realized_content = generator.order_information(ordered_info)

        self.assertEqual(expected_content, realized_content)

    def test_realize_content(self):
        documents = [Document('XIN_ENG_20041113.0001'),
                     Document('APW_ENG_20041011.0001'),
                     Document('APW_ENG_20041011.0002'),
                     Document('APW_ENG_20041011.0003')]
        expected_content = "Describe the debate over use of emergency contraceptives, " \
                           "also called the morning-after pill, " \
                           "and whether or not it should be available without a prescription.\n" \
                           "Today is Friday, October 8, the 281st day of 2004.\n" \
                           "In communist Cuba, milk rations for children stop at age 7, " \
                           "blackouts stop the fans in sweltering homes, " \
                           "and it's anyone's guess whether there'll be cooking gas this month.\n" \
                           "The U.S. House emphatically rejected a constitutional amendment banning gay marriage " \
                           "Thursday, the latest in a string of conservative pet causes advanced by Republican " \
                           "leaders in the run-up to Election Day."

        generator = LeadSummaryGenerator(documents, LeadSentenceSelector())
        ordered_info = generator.select_content()
        realized_content = generator.realize_content(ordered_info)

        self.assertEqual(expected_content, realized_content)


if __name__ == '__main__':
    unittest.main()
