from random import choice
import string


def randomGenerateString(length):
    """
    Random Generate string
    """

    letters = string.ascii_lowercase + string.digits
    result_str = "".join(choice(letters) for i in range(length))
    return result_str
