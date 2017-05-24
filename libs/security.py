import cgi


def sanitize(input_string=None):
    """Find percent symbol (%) to avoid python string format collision"""
    escaped = cgi.escape(input_string)
    input_as_list = list(escaped)
    for index, value in enumerate(input_as_list):
        if value == '%':
            input_as_list[index] = '%%'

    input_string = ''.join(input_as_list)
    return input_string
