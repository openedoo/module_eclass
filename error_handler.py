"""API error_handler.

This module produces exception or error message the user is expecting,
the better solution than using `abort` to signal errors for Invalid API usage.

.. _Reference:
   http://flask.pocoo.org/docs/0.12/patterns/apierrors/

"""
from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

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
        return rv
