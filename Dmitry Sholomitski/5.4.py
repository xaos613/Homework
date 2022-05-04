a = "I am global variable!"


def enclosing_funcion():

    a = "I am variable from enclosed function!"

    def inner_function():

        a = "I am local variable!"
        print(a)
    return inner_function
e = enclosing_funcion()
e()

def enclosing_funcion():

    a = "I am variable from enclosed function!"

    def inner_function():

        a = "I am local variable!"
        print(globals()['a'])
    return inner_function
e = enclosing_funcion()
e()

a = "I am global variable!"


def enclosing_function():
    a = "I am variable from enclosed function!"

    def inner_function():
        # a = "I am local variable!"
        print(a)
    return inner_function
e = enclosing_function()
e()