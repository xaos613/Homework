"""Implement a function get_shortest_word(s: str) -> str which returns the
longest word in the given string. The word can contain any symbols except whitespaces
(, \n, \t and so on). If there are multiple longest words in the string with a
same length return the word that occures first. Example:"""



def get_shortest_word(string):


    list_from_string = string.split()

    result = list_from_string[0].strip()
    for word in list_from_string:
        if len(word.strip()) > len(result):
            result = word.strip()




    return result


print(get_shortest_word('Python is simple and effective!'))

