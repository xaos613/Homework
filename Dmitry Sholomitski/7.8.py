'''
Implement your custom iterator class called MySquareIterator
which gives squares of elements of collection it iterates through.
Example:
```python
lst = [1, 2, 3, 4, 5]
itr = MySquareIterator(lst)
for item in itr:
    print(item)
>>> 1 4 9 16 25


'''

class MySquareIterator:
    def __init__(self, lst):
        self.lst = lst

    def __iter__(self):
        for x in self.lst:
            yield x ** 2

lst = [1, 2, 3, 4, 5]
itr = MySquareIterator(lst)


for item in itr:
    print(item)
