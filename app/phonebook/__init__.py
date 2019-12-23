from flask import Blueprint
from . import views

bp = Blueprint('phonebook', __name__, template_folder='templates')

bp.add_url_rule('/phones', view_func=views.phones, methods=['GET'])
bp.add_url_rule('/load_phones', view_func=views.load_phones, methods=['GET'])
