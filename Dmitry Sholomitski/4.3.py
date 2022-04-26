"""
Implement a function which works the same
as str. Split method (without using str. Split itself, ofcourse).
"""

def like_split(string, separator = ' '):
    result_list = []
    start_slice = 0
    for symbol in range(len(string)):
        if string[symbol] == separator:
            result_list.append(string[start_slice:symbol])
            start_slice = symbol
    else:
        if string[start_slice:] != " ":
            result_list.append(string[start_slice:])
    return result_list


print(like_split(input("Enter the string: ")))
