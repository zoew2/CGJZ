
class WordMap:
    """
    class representing a mapping of each unique word in all documents in all topics to an integer identifier
    """

    word_set = set()
    word_to_id = {}
    id_to_word = {}

    @staticmethod
    def reset():
        WordMap.word_to_id = {}
        WordMap.id_to_word = {}

    @staticmethod
    def add_words(words):
        """
        :param words: list of Strings
        :return:
        """
        WordMap.word_set = WordMap.word_set.union(words)

    @staticmethod
    def create_mapping():
        """
        creates a sorted list of words for lookups by word or id (index in list)
        pre: all documents loaded and all tokens added to word_set
        """
        WordMap.reset()
        id = 0
        for word in WordMap.word_set:
            WordMap.word_to_id[word] = id
            WordMap.id_to_word[id] = word
            id += 1

    @staticmethod
    def get_mapping():
        """
        :return: sorted list of unique words; raises ValueError if called before create_mapping has been called
        """
        if len(WordMap.word_set) > 0:
            return WordMap.word_to_id
        else:
            raise ValueError('Mapping has not been created')

    @staticmethod
    def id_of(word):
        """
        returns the id of the given word; None if the word doesn't exist in the mapping
        :param word: String
        :return: int
        """
        return WordMap.word_to_id.get(word, None)

    @staticmethod
    def get_id2word_mapping():
        """
        :return: dict
        """
        if len(WordMap.word_set) > 0:
            return WordMap.id_to_word
        else:
            raise ValueError('Mapping has not been created')
