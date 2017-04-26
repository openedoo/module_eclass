from flask import jsonify
from openedoo.core.libs import Blueprint, request, response
from .error_handler import InvalidUsage
from .database import Eclass


module_eclass = Blueprint('module_eclass', __name__)


@module_eclass.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@module_eclass.route('/', methods=['POST', 'GET'])
def eclass():
    try:
        eclass = Eclass()
        # Only accept application/json in post request data
        request_data = request.get_json(silent=True)
        if request.method == 'POST' and request_data:
            result = eclass.insert(request_data)
            return jsonify(result)

        elif request.method == 'POST' and not request_data:
            raise InvalidUsage('Failed to load request data', '',
                               status_code=415)

        else:
            result = eclass.get_all()
            return jsonify(result)

    except InvalidUsage as e:
        raise InvalidUsage('Failed to load request data', '',
                           status_code=415)

    except Exception as e:
        raise InvalidUsage('Something bad happened', repr(e), status_code=410)


@module_eclass.route('/<eclass_id>', methods=['GET', 'PUT', 'DELETE'])
def get_single_eclass(eclass_id):
    try:
        eclass = Eclass()
        result = eclass.get(eclass_id)
        return jsonify(result)

    except Exception as e:
        raise InvalidUsage('Something bad happened', repr(e), status_code=410)
