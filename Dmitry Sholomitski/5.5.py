def remember_result(funk):
    result = None
    def wrapper(*args):
        nonlocal result
        print(f"Last result  = '{result}'")
        result = funk(*args)

        return funk
    return wrapper




@remember_result
def sum_list(*args):
	result = ""
	for item in args:
		result += item
	print(f"Current result = '{result}'")
	return result

sum_list("a", "b")
sum_list("abc", "cde")
sum_list('3', '4', '5')
