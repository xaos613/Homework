"""
Implement a bunch of functions which receive a changeable number of strings and return next parameters:
-characters that appear in all strings
-characters that appear in at least one string
-characters that appear at least in two strings
-characters of alphabet, that were not used in any string


"""

test_strings = test_strings = ["hello", "world", "python"]

from string import ascii_lowercase

def test_1_1(strings):
    result_list = set()
    for letter in ascii_lowercase:
        counter = 0
        for word in strings:
            # print(word)
            if letter in word.lower():
                counter +=1
        if counter == len(strings):
            result_list.add(letter)
    return result_list


def test_1_2(strings):
    result_list = set()
    for letter in ascii_lowercase:
        counter = 0
        for word in strings:
            # print(word)
            if letter in word.lower():
                counter +=1
        if counter >= 1:
            result_list.add(letter)
    return result_list


def test_1_3(strings):
    result_list = set()
    for letter in ascii_lowercase:
        counter = 0
        for word in strings:
            # print(word)
            if letter in word.lower():
                counter +=1
        if counter >= 2:
            result_list.add(letter)
    return result_list


def test_1_4(strings):
    result_list = set()
    for letter in ascii_lowercase:
        counter = 0
        for word in strings:
            # print(word)
            if letter in word.lower():
                counter +=1
        if counter == 0:
            result_list.add(letter)
    return result_list


print(test_1_1(test_strings))
print(test_1_2(test_strings))
print(test_1_3(test_strings))
print(test_1_4(test_strings))