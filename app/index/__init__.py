from flask import Blueprint
from . import views

bp = Blueprint('index', __name__, template_folder='templates')

bp.add_url_rule('/', view_func=views.start_page, methods=['GET', 'POST'])

bp.add_url_rule('/opennews', view_func=views.open_news,
                methods=['GET', 'POST'])
