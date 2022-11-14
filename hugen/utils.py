import random
import string
import sys


class Utils:

    @staticmethod
    def get_random_text(num: int) -> str:
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(num))

    @staticmethod
    def get_random_number(num: int) -> str:
        letters = string.digits
        return "".join(random.choice(letters) for _ in range(num))

    @staticmethod
    def get_random_numeric() -> int:
        max_size = sys.maxsize
        min_size = -sys.maxsize - 1
        return random.randrange(min_size, max_size)

    @staticmethod
    def get_random_int() -> int:
        max_size = 2147483647
        min_size = -2147483648
        return random.randrange(min_size, max_size)
