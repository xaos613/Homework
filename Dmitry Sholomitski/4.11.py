"""
Implement a function, that receives changeable number of dictionaries (keys - letters, values - numbers) and combines
them into one dictionary. Dict values should be summarized in case of identical keys
"""


def combine_dicts(*args):
    result = {}
    for one_dic in args:
        for key,value in one_dic.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value


    return result

dict_1 = {'a': 100, 'b': 200}
dict_2 = {'a': 200, 'c': 300}
dict_3 = {'a': 300, 'd': 100}

print(combine_dicts(dict_1, dict_2))
print("{a': 300, 'b': 200, 'c': 300}")


print(combine_dicts(dict_1, dict_2, dict_3))
print("{'a': 600, 'b': 200, 'c': 300, 'd': 100}")