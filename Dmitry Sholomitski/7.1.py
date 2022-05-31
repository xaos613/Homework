"""
### Task 7.1
Implement class-based context manager for opening and working with file
including handling exceptions. Do not use 'with open()'. Pass filename
and mode via constructor.

"""


class Cont_manager:
    """class-based context manager for opening and working with file, including handling exceptions.
    Takes filename, mode and encoding via constructor"""

    def __init__(self, filename, mode='r', encoding='utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None

    def __enter__(self, ):
        try:
            self.file = open(self.filename, self.mode, encoding=self.encoding)
            return self.file
        except FileNotFoundError:
            print(f'ERROR: File not found')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

with Cont_manager('test.txt', 'r') as f:
    pass

