import tempfile
import random
import warnings
import string
import os


def generate_unique_code(prefix='ecl-'):
    """Generates a short and easy to remember unique_code.

    The python uuid module generates too long code. In order to keep it short,
    it uses tempfile.NamedTemporaryFile.
    """

    warnings.warn('Function generate_unique_code is deprecated, use {} instead'
                  .format('unique_code_generator'), DeprecationWarning,
                  stacklevel=3)

    temporary = tempfile.NamedTemporaryFile(prefix=prefix)
    unique_code = os.path.basename(temporary.name)
    return unique_code


def unique_code_generator(length=8, charset=None):
    """Generates a short and easy to remember unique_code."""
    if not charset:
        ascii_uc = string.ascii_uppercase
        digit = string.digits
        charset = ascii_uc + digit

    sys_rand = random.SystemRandom()
    random_chars = [sys_rand.choice(charset) for _ in range(length)]
    unique_code = ''.join(random_chars)
    return unique_code
