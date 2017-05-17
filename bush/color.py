END_CODE = '\033[0m'


def green(str):
    return '\033[92m{}{}'.format(str, END_CODE)


def yellow(str):
    return '\033[93m{}{}'.format(str, END_CODE)


def red(str):
    return '\033[91m{}{}'.format(str, END_CODE)
