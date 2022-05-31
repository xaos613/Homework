"""
Implement an iterator class EvenRange, which accepts start and end of the interval as an init arguments
and gives only even numbers during iteration.
If user tries to iterate after it gave all possible numbers `Out of numbers!` should be printed.
_Note: Do not use function `range()` at all_
Example:
"""


class EvenRange:

    def __init__(self, start, stop):
        self.start = start if start % 2 == 0 else start +1
        self.stop = stop


    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= self.stop:
            print('Out of numbers')
            raise StopIteration("Out of numbers")
        res = self.start
        self.start += 2
        return res



er1 = EvenRange(7, 11)
print(next(er1))
print(8)
print(next(er1))
print(10)
# print(next(er1))
# print("Out of numbers!")
# print(next(er1))
# print("Out of numbers!")
er2 = EvenRange(3, 14)
for number in er2:
    print(number, end=" ")
# print('4 6 8 10 12 "Out of numbers!"')
