# Task 7.4
# Implement decorator for supressing exceptions. If exception not occure write log to console.
from contextlib import ContextDecorator


class SupressExceptions(ContextDecorator):

    def __init__(self, note: str = None):
        self.note = note
        self.file = None

    def __call__(self, function):
        if self.note is None:
            self.note = function.__name__
        return super().__call__(function)

    def __enter__(self):
        try:
            self.file = open('Exceptionlog.txt', 'a+', encoding='utf-8')
        except Exception:
            print(f'ERROR: unable to create logfile')
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if exc_type is None:
            print(f'The {self.note} function raised no exceptions while running', file=self.file)
        else:
            print(f'Exception "{exc_val}" supressed')
            print(f'Exception "{exc_val}" supressed', file=self.file)
        if self.file:
            self.file.close()
        return True


@SupressExceptions()
def div(a, b):
    return a / b


if __name__ == '__main__':
    print(div(1, 4))
    print(div(1, 0))