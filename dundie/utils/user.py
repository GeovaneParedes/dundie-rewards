from random import sample
from string import ascii_letters, digits


def generate_simple_password(size=8):
    """Generation of simple random passwords.
    [a-z][A-Z][0-9]
    """
    password = sample(ascii_letters + digits, size)
    return "".join(password)
