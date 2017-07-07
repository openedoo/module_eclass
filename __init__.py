from flask import jsonify
from openedoo.core.libs import Blueprint, request, response
from .libs.error_handler import InvalidUsage, simple_error_message
from .model.eclass import Eclass
from .model.eclass_member import EclassMember

RESULT_PER_PAGE = 20
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
            page = int(request.args.get('page')) if request.args else 1
            start_page = (page - 1) * RESULT_PER_PAGE
            pagination = {
                'limit': RESULT_PER_PAGE,
                'start_page': start_page,
            }
            result = eclass.get_all(pagination=pagination)
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


@module_eclass.route('/<int:eclass_id>/members', methods=['GET', 'POST'])
def eclass_members(eclass_id):
    try:
        member = EclassMember()
        # Only accept application/json in post request data
        request_data = request.get_json(silent=True)
        if request.method == 'POST' and request_data:
            request_data['class_id'] = eclass_id
            if 'is_creator' not in request_data:
                request_data['is_creator'] = 0

            result = member.add(request_data)
            return jsonify(result)

        elif request.method == 'POST' and not request_data:
            raise InvalidUsage('Failed to load request data', '',
                               status_code=415)

        else:
            page = int(request.args.get('page')) if request.args else 1
            start_page = (page - 1) * RESULT_PER_PAGE
            pagination = {
                'limit': RESULT_PER_PAGE,
                'start_page': start_page,
            }
            result = member.get(eclass_id, pagination)
            return jsonify(result)

    except Exception as e:
        raise


app_route = '/<int:class_id>/members/<int:user_id>'
@module_eclass.route(app_route, methods=['DELETE'])
def eclass_single_member(class_id, user_id):
    try:
        member = EclassMember()
        result = member.delete(class_id, user_id)
        return jsonify(result)

    except Exception as e:
        raise InvalidUsage('Failed to load request data', str(e),
                           status_code=415)


@module_eclass.route('/<int:eclass_id>/discussions', methods=['GET', 'POST'])
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
        raise InvalidUsage('Failed to load request data', str(e),
                           status_code=415)
