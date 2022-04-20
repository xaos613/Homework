"""
Write a program which makes a pretty print of a part of the multiplication table. Examples:
"""


a = 2
b = 15
c = 2
d = 13

print('\t', end = "")
for y in range(c, d + 1):
    print(y, end='\t')
print()
for x in range(a, b+1):
    print(x, end='\t')
    for y in range(c, d+1):
        print(x*y, end='\t')
    print()

