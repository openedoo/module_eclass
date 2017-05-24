import tempfile
import os


def generate_unique_code(prefix='ecl-'):
    """Generates a short and easy to remember unique_code.

    The python uuid module generates too long code. In order to keep it short,
    it uses tempfile.NamedTemporaryFile.
    """
    temporary = tempfile.NamedTemporaryFile(prefix=prefix)
    unique_code = os.path.basename(temporary.name)
    return unique_code
