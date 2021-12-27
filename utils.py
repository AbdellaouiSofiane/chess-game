import string


def index_generator():
    for char in string.ascii_lowercase:
        yield char
