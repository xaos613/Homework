"""Write a Python program to sort a dictionary by key.
"""
# Write a Python program to sort a dictionary by key.


my_dict = {2: 3, 1: 89, 4: 5, 3: 0}

keys = my_dict.keys()

for key in sorted(keys):
    print(f"{key} : {my_dict[key]}")
