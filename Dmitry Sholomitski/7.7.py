from typing import Iterable

class MyNumberCollection():


    def __init__(self, *args):
        try:
            if isinstance(args[0], (list, tuple)):
                if not all([isinstance(x, int) for x in args[0]]):
                    raise TypeError ('There should be only integer numbers')
                self._data = list(args[0])

            elif len(args) < 3:
                self._data = list(args)
            else:
                self._data = [x for x in range(args[0], args[1], args[2])]
                self._data.append(args[1])
        except TypeError as error:
            print(error)


    def __iter__(self):
        for x in self._data:
            yield x

    def __getitem__(self, item):
         return self._data[item] ** 2

    def __repr__(self):
         return str(list(self))

    def append(self, new_value):
        try:
            if isinstance(new_value, int):
                self._data.append(new_value)
            else:
                raise TypeError(f"You should add only integer numbers, but '{new_value}' added.")
        except TypeError as error:
            print(error)


    def __add__(self, other):
        if not all([isinstance(x, int) for x in other]):
            raise TypeError('There should be only integer numbers')
        return self._data + list(other)

    __radd__ = __add__


if __name__ == '__main__':
    col1 = MyNumberCollection(0, 5, 2)
    print(col1)
    col2 = MyNumberCollection((1, 2, 3, 4, 5))
    print(col2)
    col3 = MyNumberCollection((1, 2, 3, "4", 5))

    col1.append(7)
    print(col1)
    col2.append("string")
    print(col1 + col2)
    print(col1)
    print(col2)
    print(col2[4])
    for item in col1:
        print(item, end = ' ')