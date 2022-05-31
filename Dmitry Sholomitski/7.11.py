'''
Implement a generator which will geterate [Fibonacci numbers].
Example:
'''

def endless_fib_generator():
    a,b = 0, 1
    while True:
        yield a+b
        a, b = b, b+a



gen = endless_fib_generator()
while True:
    print(next(gen), end='\n')