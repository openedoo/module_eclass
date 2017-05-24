from flask import jsonify
from openedoo.core.libs import Blueprint, request, response
from .libs.error_handler import InvalidUsage, simple_error_message
from .model.eclass import Eclass


module_eclass = Blueprint('module_eclass', __name__)


@module_eclass.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


@module_eclass.route('/', methods=['POST', 'GET'])
def index():
    try:
        eclass = Eclass()
        # Only accept application/json in post request data
        request_data = request.get_json(silent=True)
        if request.method == 'POST' and request_data:
            result = eclass.add(request_data)
            return jsonify(result)

        elif request.method == 'POST' and not request_data:
            raise InvalidUsage('Failed to load request data', '',
                               status_code=415)

        else:
            result = eclass.get_all()
            return jsonify(result)

    except Exception as e:
        raise


@module_eclass.route('/<int:eclass_id>', methods=['GET', 'PUT', 'DELETE'])
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

    except Exception:
        raise


@module_eclass.route('/<eclass_id>/members', methods=['GET', 'POST'])
def eclass_members(eclass_id):
    try:
        eclass = Eclass()
        # Only accept application/json in post request data
        request_data = request.get_json(silent=True)
        if request.method == 'POST' and request_data:
            request_data['id'] = eclass_id
            result = eclass.add_member(request_data)
            return jsonify(result)

        elif request.method == 'POST' and not request_data:
            raise InvalidUsage('Failed to load request data', '',
                               status_code=415)

        else:
            result = eclass.get_members(eclass_id)
            return jsonify(result)

    except Exception as e:
        error = simple_error_message(str(e))
        return jsonify(error)


app_route = '/<eclass_id>/members/<member_id>'
@module_eclass.route(app_route, methods=['GET', 'DELETE'])
def eclass_single_member(eclass_id, member_id):
    try:
        eclass = Eclass()
        if request.method == 'DELETE':
            result = eclass.delete_member(eclass_id, member_id)
            return jsonify(result)

        result = eclass.get_member(eclass_id, member_id)
        return jsonify(result)

    except Exception as e:
        error = simple_error_message(str(e))
        return jsonify(error)


@module_eclass.route('/<eclass_id>/admins', methods=['GET'])
def eclass_admins(eclass_id):
    try:
        eclass = Eclass()
        result = eclass.get_admins(eclass_id)
        return jsonify(result)

    except Exception as e:
        error = simple_error_message(str(e))
        return jsonify(error)


@module_eclass.route('/<eclass_id>/discussions', methods=['GET', 'POST'])
def eclass_discussion(eclass_id):
    try:
        eclass = Eclass()
        request_data = request.get_json(silent=True)
        if request.method == 'POST' and request_data:
            result = eclass.add_discussion(eclass_id, request_data)
            return jsonify(result)
        else:
            result = eclass.get_discussion(eclass_id)
            return jsonify(result)

    except Exception as e:
        error = simple_error_message(str(e))
        return jsonify(error)
