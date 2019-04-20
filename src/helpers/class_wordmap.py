class WordMap:
    """
    class representing a mapping of each unique word in all documents in all topics to an integer identifier
    """

    word_set = {}
    word_list = []

    @classmethod
    def add_word(cls, word):
        """
        :param word: String
        :return:
        """
        if not word in word_set:
            word_set.add(word)


    @classmethod
    def add_words(cls, words):
        """
        :param words: list of Strings
        :return:
        """
        unique_input_words = set(words)
        for word in unique_input_words:
            add_word(word)

    @classmethod
    def create_mapping(cls):
        """
        creates a sorted list of words for lookups by word or id (index in list)
        *intended to be called only after all documents have been loaded and all tokens added to word_set*
        """
        # sorted list from set
        global word_list
        word_list = sorted(list(word_set))

    @classmethod
    def get_mapping(cls):
        """
        :return: sorted list of unique words; raises ValueError if called before create_mapping has been called
        """
        if len(word_list) > 0:
            return word_list
        else:
            raise ValueError('Mapping has not been created')

    @classmethod
    def id_of(cls, word):
        """
        returns the id of the given word; None if the word doesn't exist in the mapping
        :param word: String
        :return: int
        """
        return word_list.index(word)

    @classmethod
    def word_at(cls, id):
        """
        returns the word that corresponds to the given id
        :param id: int
        :return: String
        """
        return word_list[id]