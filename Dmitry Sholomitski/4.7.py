"""
Implement a function foo(List[int]) -> List[int] which, given a list
of integers, return a new list such that each element at index i of the
new list is the product of all the numbers in the original array except
the one at i. Example:
"""


def foo(int_list):
    result_list = []

    for index in range(len(int_list)):
        temp_int = 1
        for index2 in range(len(int_list)):
            if index is not index2:
                temp_int *= int_list[index2]
        result_list.append(temp_int)

    return result_list

print(foo([1, 2, 3, 4, 5]))

