""" Create random strings """
from random import randint

DIGITS = '0123456789'
UPPER = 'QWERTYUIOPASDFGHJKLZXCVBNM'
LOW = 'qwertyuiopasdfghjklzxcvbnm'
ALPHA = UPPER + LOW
ALPHA_NUMERIC = ALPHA + DIGITS
X = "ABCDEF" + DIGITS
SPECIAL = '~`!@#%^&*()-_=+[{]};:'

def random_string(len_min, set_of_characters=X, len_max=None):
    """
    Create a random string of characters
    :param len_min:
    :param set_of_characters:
    :param len_max: if None, set to len_min
    :return:
    """
    len_of_set = len(set_of_characters)
    assert len_of_set, 'set_of_characters is empty'
    if len_max:
        assert len_min <= len_max, 'len_min > len_max'
        str_len = randint(len_min, len_max)
    else:
        str_len = len_min
    return ''.join([set_of_characters[randint(0, len_of_set - 1)] for _ in range(str_len)])

def random_name(len_min, len_max=None):
    """
    Create a capitaluzed random name
    :param len_min:
    :param len_max:  if None, set to len_min
    :return:
    """
    return random_string(1, UPPER) + random_string(
        len_min - 1, LOW, len_max -1 if len_max else len_max)
