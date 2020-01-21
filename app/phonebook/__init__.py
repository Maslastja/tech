from flask import Blueprint
from . import views

bp = Blueprint('phonebook', __name__, template_folder='templates')

# bp.add_url_rule('/phones', view_func=views.phones, methods=['GET'])
# bp.add_url_rule('/load_phones', view_func=views.load_phones, methods=['GET'])

bp.add_url_rule('/phones', view_func=views.phonesnew,
                methods=['GET', 'POST'])
bp.add_url_rule('/openphone', view_func=views.open_phone,
                methods=['GET', 'POST'])

bp.add_url_rule('/phoneslist', view_func=views.get_phones, methods=['GET'])
