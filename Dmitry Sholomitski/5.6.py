def call_once(funk):
    result = None
    def wrapper(a,b):
        nonlocal result
        if result is None:
            result = funk(a,b)
        return result

    return wrapper




@call_once
def sum_of_numbers(a, b):
    return a + b


print(sum_of_numbers(13, 42))
# >>> 55
print(sum_of_numbers(999, 100))
# >>> 55
print(sum_of_numbers(134, 412))
# >>> 55
print(sum_of_numbers(856, 232))
# >>> 55