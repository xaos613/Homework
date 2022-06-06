"""
### Task 7.6
Create console program for proving Goldbach's conjecture. Program accepts number for input and print result.
For pressing 'q' program successfully close. Use function from Task 5.5 for validating input, handle all exceptions
and print user-friendly output.

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


class ValueException(CustomException):
    pass


def get_primes(num: int) -> list:
    """
    The function takes an integer and returns a list of primes in range [2, integer + 1)
    :param num: input integer
    :return: list of corresponding primes
    """

    primes_gen = (x for x in range(2, num + 1))
    primes = [2]

    for number in primes_gen:
        i = 2
        while number % i != 0:
            i += 1
            if i == number:
                primes.append(number)
    return primes


def chckerfunc(number):
    if number is None:
        raise EmptyException('There should  be at least 1 argument')
    else:
        try:
            number = int(number)
        except (ValueError, TypeError):
            raise TypeException(('There should be integer argument'))

    if number < 4:
        raise ValueException(f"Input integer should be more than 3, you gave {number}")
    elif number % 2 == 0:
        return number


def get_input():
    x = input("Input a positive even integer to prove Goldbach's conjecture for it, or 'q' to exit script: ")
    return x


def goldbach(number):
    number = chckerfunc(number)
    primes = get_primes(number)
    goldbach_result = [[number - x, x] for x in primes if number - x in primes]
    return (number, goldbach_result[-1])


def main():
    while True:
        choise = get_input()
        if choise in ['q', 'Q']:
            print("Thank you for using my script. Bye")
            break
        else:
            num = choise if choise else None
            try:
                print(goldbach(num))
            except ValueException as message:
                print(f'Incorrect input: {message}')
            except EmptyException as message:
                print(f'Incorrect input: {message}')
            except TypeException as message:
                print(f'Incorrect input: {message}')


if __name__ == '__main__':
    main()
