from flask import Blueprint, render_template
from . import views

bp = Blueprint('admin', __name__, template_folder='templates')
options = {'url_prefix': '/admin'}

bp.add_url_rule('/type/news', view_func=views.get_types_news,
                methods=['GET', 'POST'])
bp.add_url_rule('/type/links', view_func=views.get_types_links,
                methods=['GET', 'POST'])
bp.add_url_rule('/type', view_func=views.open_type,
                methods=['GET', 'POST'])
bp.add_url_rule('/links', view_func=views.get_links,
                methods=['GET', 'POST'])
bp.add_url_rule('/get_links', view_func=views.get_links_ajax,
                methods=['GET'])
bp.add_url_rule('/links/link', view_func=views.open_link,
                methods=['GET', 'POST'])


@bp.route('/')
def start_page():
    return render_template('admin.html', title='Администрирование')
