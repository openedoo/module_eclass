from flask import jsonify
from openedoo.core.libs import Blueprint, request, response
from .error_handler import InvalidUsage
from .database import Eclass


module_eclass = Blueprint('module_eclass', __name__)


@module_eclass.route('/', methods=['POST', 'GET'])
def eclass():
    eclass = Eclass()
    # Only accept application/json in post request data
    request_data = request.get_json(silent=True)
    if request.method == 'POST' and request_data:
        result = eclass.insert(request_data)
        return jsonify(result)
    result = eclass.get_all()
    return jsonify(result)
