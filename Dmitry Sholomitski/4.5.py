"""
Implement a function get_digits(num: int) -> Tuple[int]
which returns a tuple of a given integer's digits. Example:
"""

def get_digits(num):
    result = []
    for i in str(num):
        result.append(int(i))

    return tuple(result)

print(get_digits(87178291199))

