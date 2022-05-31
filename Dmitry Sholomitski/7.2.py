"""
### Task 7.2
Implement context manager for opening and working with file,
including handling exceptions with @contextmanager decorator.

"""

from contextlib import contextmanager


@contextmanager
def open_file(filename, mode='r', encoding='utf-8'):
    file = None
    try:
        file = open(filename, mode, encoding=encoding)
        yield file
    except FileNotFoundError:
        print(f'File not found')
    if file:
        file.close()


def main():
    try:
        counter = 0
        with open_file("test.txt", 'x') as file:
            for i, line in enumerate(file):
                if i == 0:
                    print(line.strip())
                counter += 1
            print(counter)
        print(file.closed)
    except TypeError as message:
        print(f"open_file returned nothing: {message}")
    except Exception as message:
        print(f"Something went wrong: {message}")


if __name__ == '__main__':
    main()
