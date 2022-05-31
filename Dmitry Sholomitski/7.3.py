"""
## Task 7.3
Implement decorator with context manager support for writing execution time to log-file. See contextlib module.

"""

# Task 7.3
# Implement decorator with context manager support for writing execution time to log-file. See contextlib module.
from contextlib import ContextDecorator
import time


class TimingContext(ContextDecorator):
    """Class implements a decorator with context manager support for writing execution time to log-file.
    Takes a note on call and writes log string with that note included. Uses the decorated function name as default note
    for log string if note not given.
    default log string looks like: 'The {note} function took {total_run_time:.4f} seconds to run'"""

    def __init__(self, note: str = None):
        self.note = note
        self.file = None

    def __call__(self, function):
        if self.note is None:
            self.note = function.__name__
        return super().__call__(function)

    def __enter__(self):
        try:
            self.file = open('log.txt', 'a+', encoding='utf-8')
        except:
            print(f'ERROR: unable to create logfile')
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_time = time.perf_counter()
        self.total_run_time = self.stop_time - self.start_time
        print(f'The {self.note} function took {self.total_run_time:.4f} seconds to run', file=self.file)
        if self.file:
            self.file.close()
        return False


@TimingContext()
def count_funk():
    counter = 0
    for i in range(100000000):
        counter += i
    return counter


if __name__ == '__main__':
    print(count_funk())
