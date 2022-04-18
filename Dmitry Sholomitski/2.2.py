def letter_counter(string):
    result = {}
    for symbol in string:
        if symbol.lower() in result:
            result[symbol] += 1
        else:
            result[symbol] = 1
    return result




print(letter_counter(input('Enter the string: ').lower()))
