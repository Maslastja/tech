from flask import Blueprint
from . import views

bp = Blueprint('phonebook', __name__, template_folder='templates')
options = {'url_prefix': '/phones'}

bp.add_url_rule('/', view_func=views.phonesnew,
                methods=['GET', 'POST'])
bp.add_url_rule('/openphone', view_func=views.open_phone,
                methods=['GET', 'POST'])

bp.add_url_rule('/phoneslist', view_func=views.get_phones, methods=['GET'])
