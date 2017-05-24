from flask import jsonify


def simple_error_message(value=None):
    """A simple error message setter.

    In order to provide consistency in the error message and easier to change
    in the future.
    """
    return {'error message': value}


class InvalidUsage(Exception):
    """API error_handler.

    This module produces exception or error message the user is expecting,
    the better solution than using `abort` to signal errors for
    Invalid API usage.

    .. _Reference:
       http://flask.pocoo.org/docs/0.12/patterns/apierrors/

    """
    status_code = 400
    more_info = "http://openedoo-eclass-module.readthedocs.io/en/latest/"

    def __init__(self, message, exception, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.exception = exception
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['exception'] = self.exception
        rv['more_info'] = self.more_info
        return rv
