from flask import jsonify
from openedoo.core.libs import Blueprint, request, response
from .error_handler import InvalidUsage
from .model import Eclass


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

    except Exception as e:
        error = {'error message': str(e)}
        return jsonify(error)


@module_eclass.route('/<eclass_id>', methods=['GET', 'PUT', 'DELETE'])
def get_single_eclass(eclass_id):
    try:
        eclass = Eclass()
        # Only accept application/json in post request data
        request_data = request.get_json(silent=True)
        if request.method == 'PUT' and request_data:
            request_data['id'] = eclass_id
            result = eclass.update(request_data)
            return jsonify(result)

        elif request.method == 'DELETE':
            result = eclass.delete(eclass_id)
            return jsonify(result)

        else:
            result = eclass.get(eclass_id)
            return jsonify(result)

    except Exception as e:
        error = {'error message': str(e)}
        return jsonify(error)


@module_eclass.route('/<eclass_id>/members', methods=['GET', 'POST'])
def eclass_members(eclass_id):
    try:
        eclass = Eclass()
        result = eclass.get_members(eclass_id)
        return jsonify(result)

    except Exception as e:
        error = {'error message': str(e)}
        return jsonify(error)
