END_CODE = "\033[0m"


def green(str):
    return "\033[92m%s%s" % (str, END_CODE)


def yellow(str):
    return "\033[93m%s%s" % (str, END_CODE)


def red(str):
    return "\033[91m%s%s" % (str, END_CODE)
