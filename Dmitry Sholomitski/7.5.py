"""### Task 7.5
Implement function for check that number is even, at least 3.
Throw different exceptions for this errors. Custom exceptions must be derived from custom base exception
(not Base Exception class).
"""


class CustomException(BaseException):

    def __init__(self, error_message=''):
        self.message = error_message

    def __str__(self):
        return self.message


class TypeException(CustomException):
    pass

class EmptyException(CustomException):
    pass

class BoolException(CustomException):
    pass


def chckerfunc(number = None):
    if number is None:
        raise EmptyException('There should  be at least 1 argument')
    elif isinstance(number, bool):
        raise  BoolException(('There should be NOT bool argument'))
    elif not isinstance(number, int):
        raise TypeException('There should be integer argument')
    return number % 2 == 0


def main():
    print(chckerfunc(3))
    print(chckerfunc(2))
    try:
        print(chckerfunc())
    except EmptyException as message:
        print(f'Error : {message}')
    try:
        print(chckerfunc(True))
    except BoolException as message:
        print(f'Error - {message}')
    try:
        print(chckerfunc('2'))
    except TypeException as message:
        print(f'Error - {message}')

if __name__ == '__main__':
    main()
