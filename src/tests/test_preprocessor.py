import unittest
<<<<<<< HEAD
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    Preprocessor.load_models()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        expected_tokenized_sen= ['take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor.sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence1 = "In the morning he took his small puppy to New York today ."
        expected_tokenized_sen1 = ['the morning', 'take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor.sent_preprocessing(raw_sentence1)
        self.assertEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor.sent_preprocessing(raw_sentence2)
        self.assertEqual(expected_tokenized_sen2, tokenized_sen2)





if __name__ == '__main__':
    unittest.main()
=======
from src.helpers.class_document import Document
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors

class TestPreprocessor(unittest.TestCase):
    '''
    check that preprocessed text is making it into vectors
    - sentence.tokens reflects NER, stemming, stopword and punctuation removal, and lowercasing
    - wordmap.word_to_id contains only preprocessed tokens
    '''

    topic1_docs = [Document("TST_ENG_20190501.0001"),
                   Document("TST_ENG_20190501.0002"),]
    topic2_docs = [Document("TST_ENG_20190601.0001")]

    topics = {1: topic1_docs, 2: topic2_docs}

    WordMap.create_mapping()
    vec = Vectors()
    vec.create_freq_vectors(topics)

    def test_coref(self):
        exp_coref = '''NEW YORK _ Some of the police officers who shot and killed Amadou Diallo have told associates that Some of the police officers who shot and killed Amadou Diallo attention was initially drawn to Diallo when Some of the police officers who shot and killed Amadou Diallo saw Diallo standing on the stoop of a Bronx apartment building and thought Some of the police officers who shot and killed Amadou Diallo saw Diallo peering into the window of a first-floor apartment, according to people with knowledge of the case. 

   Some of the police officers who shot and killed Amadou Diallo told associates that Some of the police officers who shot and killed Amadou Diallo grew more suspicious when two of Some of the police officers who shot and killed Amadou Diallo got out of Some of the police officers who shot and killed Amadou Diallo car to question Diallo and Diallo retreated into the vestibule of a Bronx apartment building, the people knowledgeable about the case said on Tuesday. 

   Some of the police officers who shot and killed Amadou Diallo, did not testify about the shooting before the grand jury that heard Some of the police officers who shot and killed Amadou Diallo case. Diallo, an unarmed man with no criminal history, was killed on Feb. 4 when the four officers fired 41 shots at Diallo, 19 of which hit Diallo. 

   the shooting before the grand jury that heard their case led to 15 days of protests outside Police Headquarters and reignited the gnawing debate about police in New York City. During the outcry the four officers, the four officers lawyers and law-enforcement officials have remained silent about what set off the shooting before the grand jury that heard their case. 

   But several officers are said to have told associates that the chain of events that led to the shooting before the grand jury that heard their case began when several officers first spotted Diallo and thought that several officers saw Diallo looking into the window. 

   several officersDiallo . several officers did not know it, but it was the building where Diallo lived. 

   McMellon and Carroll got out of McMellon and Carroll maroon Ford Taurus and approached Diallo on the stoop of No. 1157. McMellon stood to the left and Carroll to the right as McMellon and Carroll mounted the steps. 

   What happened next is sure to be the subject of much debate at the future criminal trial of the four officers. the four officers have yet to officially explain the four officers actions. But several officers told associates that after several officers identified several officers and asked to talk to Diallo, Diallo retreated into the building's vestibule and appeared to be trying to reach the inner door, the people with knowledge of the case said. 

   Diallo remained silent during the whole encounter, the people with knowledge of the case said. 

   According to this account, several officers told associates that while Diallo was in the building's vestibule, Diallo made a move that led several officers to believe Diallo was armed: Diallo turned to Diallo right, reached into Diallo pocket and pulled something out. It turned out later to be Diallo black wallet. 

   At that point, Carroll yelled, ``Gun!'' the people knowledgeable about the case said. 

   Some of the details were first reported Tuesday in The New York Post. 

   It was unclear from Tuesday's accounts who fired the first shot. 

   As the first gunshots rang out, McMellon fell backwards down the steps and injured McMellon tailbone, causing at least some of McMellon colleagues to believe that McMellon had been hit by return fire, people knowledgeable about the case said. Carroll moved to his right and continued firing, and Murphy and Boss, who were closer to the car, began firing as well, people knowledgeable about the case said. 

   Several of the officers are said to have told associates that Several of the officers continued firing because Diallo did not fall even after Several of the officers had unleashed the fusillade. When the officers saw afterward that Diallo was unarmed, people knowledgeable about the case said, at least one of the officers wept.'''

        self.assertEqual(exp_coref, self.topics.get(1)[0].text)

if __name__ == '__main__':
    unittest.main()


>>>>>>> coref resolution and tests
