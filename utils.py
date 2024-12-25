from random import randint

def random_bit():
    return randint(0, 255)

def random_rgb():
    return (
        random_bit(),
        random_bit(),
        random_bit()
    )


def titlelize(word: str, marge: int=2) -> str:
    """ Stylise un titre """
    return f"{'-' * (len(word) + 2 * marge + 2)}\n|{' ' * marge}{word}{' ' * marge}|\n{'-' * (len(word) + 2 * marge + 2)}"