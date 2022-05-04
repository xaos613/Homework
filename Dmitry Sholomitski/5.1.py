'''
Open file data/unsorted_names.txt in data folder. Sort the names and write them to a new file called sorted_names.txt.
Each name should start with a new line as in the following example:
'''

list_for_sort = []

with open('data/unsorted_names.txt') as unsorted_file:
    for row in unsorted_file:

        list_for_sort.append(row.strip())

with open('data/sorted_names.txt', 'w') as sorted_file:
    for name in sorted(list_for_sort):
        sorted_file.write(name + '\n')

