"""
Implement a function split_by_index(s: str, indexes: List[int]) -> List[str]
which splits the s string by indexes specified in indexes. Wrong indexes must be ignored. Examples:

>>> split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])
["python", "is", "cool", ",", "isn't", "it?"]

>>> split_by_index("no luck", [42])
["no luck"]
"""

def split_by_index(s, indexes):
    start_slice = 0
    result_list = []
    for i in indexes:
        result_list.append(s[start_slice:i])
        start_slice = i

    return result_list

print(split_by_index("no luck", [42]))

