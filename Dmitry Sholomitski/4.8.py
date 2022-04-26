"""
Implement a function get_pairs(lst: List) -> List[Tuple] which returns a list of tuples containing pairs of elements.
Pairs should be formed as in the example. If there is only one element in the list return None instead. Example:
>>> get_pairs([1, 2, 3, 8, 9])
[(1, 2), (2, 3), (3, 8), (8, 9)]

"""



def get_pairs(enter_list):

    result_list = []
    for x in range(len(enter_list)-1):
        result_list.append((enter_list[x], enter_list[x+1]))
    return result_list


print(get_pairs(['need', 'to', 'sleep', 'more']))

