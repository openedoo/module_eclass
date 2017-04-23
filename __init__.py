from openedoo.core.libs import Blueprint
from .database import Eclass


module_eclass = Blueprint('module_eclass', __name__)


@module_eclass.route('/', methods=['POST', 'GET'])
def index():
    return "Hello module module_eclass"
