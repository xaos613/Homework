"""
Write a Python program to convert a given tuple of positive integers into an integer. Examples:

Input: (1, 2, 3, 4)
Output: 1234
"""

input_tuple = (1, 2, 3, 4, 7)

print(int(''.join(str(x) for x in input_tuple)))
