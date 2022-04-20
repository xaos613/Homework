def quota_reverse(string):
    """

    :param string:
    :return: string with replaced all " symbols with ' and vise versa
    """

    result_str = ""
    for i in string:
        if i == '"':
            result_str += '\''
        elif i == '\'':
            result_str += '"'
        else:
            result_str += i
    return result_str


print(quota_reverse('My sister\'s friend said: "Hi"'))
