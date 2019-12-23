from flask import Blueprint
from . import views
bp = Blueprint('calendar', __name__, template_folder='templates')
options = {'url_prefix': '/calendar'}

bp.add_url_rule('/', view_func=views.start_page,
                methods=['GET', 'POST'])
bp.add_url_rule('/openevent', view_func=views.open_event,
                methods=['GET', 'POST'])
