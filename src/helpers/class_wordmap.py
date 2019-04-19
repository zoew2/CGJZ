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
            word_list.append(word)


    @classmethod
    def add_words(cls, words):
        """
        :param words: list of Strings
        :return:
        """
        unique_input_words = set(words)
        for word in unique_input_words:
            add_word(word)
