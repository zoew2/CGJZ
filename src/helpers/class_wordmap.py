class WordMap:
    """
    class representing a mapping of each unique word in all documents in all topics to an integer identifier
    """

    word_set = set()
    word_to_id = {}

    @classmethod
    def add_words(cls, words):
        """
        :param words: list of Strings
        :return:
        """
        word_set.union(words)

    @classmethod
    def create_mapping(cls):
        """
        creates a sorted list of words for lookups by word or id (index in list)
        pre: all documents loaded and all tokens added to word_set
        """
        global word_set
        id = 0
        for word in word_set:
            word_to_id[word] = id
            id += 1

    @classmethod
    def get_mapping(cls):
        """
        :return: sorted list of unique words; raises ValueError if called before create_mapping has been called
        """
        if len(word_set) > 0:
            return word_to_id
        else:
            raise ValueError('Mapping has not been created')

    @classmethod
    def id_of(cls, word):
        """
        returns the id of the given word; None if the word doesn't exist in the mapping
        :param word: String
        :return: int
        """
        return word_to_id[word]