# Copyright 2020 by Kirill Kanin, Ilya Dementyev
# All rights reserved.

import random
import string
from datetime import datetime

filename_len = 8


class SingletonMeta(type):
    """Meta class for singletons.

    """

    def __call__(cls):
        pass


def generate_string() -> str:
    """Generate random string.

    Method generates random string with digits and latin letters.

    Returns:
        str: random string.

    """

    _letters = string.ascii_letters
    _digits = string.digits
    _chars = _letters + _digits
    _str = ''.join(random.choice(_chars) for i in range(filename_len))
    return _str


def convert_date(timestamp: float) -> str:
    """Convert date from timestamp to string.

    Example of date format: 2019-09-05 11:22:33.

    Args:
        timestamp (float): date timestamp.

    Returns:
        str: converted date.

    """

    _out_format = '%Y-%m-%d %H:%M:%S'
    return datetime.fromtimestamp(timestamp).strftime(_out_format)
