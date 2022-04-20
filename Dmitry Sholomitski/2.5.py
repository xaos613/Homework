"""
Write a Python program to print all unique values of all dictionaries in a list. Examples:

Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
Output: {'S005', 'S002', 'S007', 'S001', 'S009'}
"""

input_dicts = [{"V": "S001"}, {"Vf": "S007"}, {"VI": "S001"}, {"VI": "S005"}, {"VII": "S005"}, {"V": "S009"},
               {"VIII": "S007"}]

result_set = set()
for seporate_dict in input_dicts:
    for value in seporate_dict.values():
        result_set.add(value)

print(list(result_set))
