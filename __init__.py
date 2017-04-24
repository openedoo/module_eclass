from flask import jsonify
from openedoo.core.libs import Blueprint
from .database import Eclass


module_eclass = Blueprint('module_eclass', __name__)


@module_eclass.route('/', methods=['POST', 'GET'])
def index():
    eclass = Eclass().get_all()
    return jsonify(eclass)
