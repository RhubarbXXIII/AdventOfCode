from math import log10


def count_digits(n: int) -> int:
    if n == 0:
        return 1

    return int(log10(n if n > 0 else -n)) + 1