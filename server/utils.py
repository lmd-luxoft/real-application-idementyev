__version__ = '0.3.0'
__author__ = 'idementyev@luxoft.com'
__date__ = '2020-09-24'


import random
import string
from datetime import datetime, timezone


filename_len = 8


class SingletonMeta(type):
    """Meta class for singletons."""
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
    _str = ''.join(random.choice(_chars) for _ in range(filename_len))
    return _str


def convert_date(timestamp: float) -> str:
    """Convert date from timestamp to string.

    Example of date format: 2019-09-05 11:22:33.
    Date is considered to be in UTC as atime, mtime, ctime are stored in UTC.

    Args:
        timestamp (float): date timestamp.
    Returns:
        str: converted date.
    """
    _format = '%Y-%m-%d %H:%M:%S'
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime(_format)
