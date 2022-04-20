"""
Write a function that check whether a string is a palindrome or not. Usage of any reversing functions is prohibited.
To check your implementation you can use strings from here.
"""

def is_polindrom(string):


    for i in range(int((len(string)//2)/2)):
        if string[i].lower() == string[-1-i].lower():
            continue
        else:
            return False

    return True




print(is_polindrom('Аргентина манит негра'))

