def str_len(string):
    '''

    :param string: input string
    :return: lenth of string
    '''
    counter = 0
    for letter in string:
        counter += 1
    return counter



print(str_len(input('Enter the string: ')))
