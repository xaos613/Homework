def sorted_uniq_list(input_words):
    """

    :param input_words: comma separated sequence of words
    :return: unique words in sorted form
    """
    return sorted(list(set(word.strip() for word in input_words.split(','))))


print(sorted_uniq_list(input('Enter the string: ')))
