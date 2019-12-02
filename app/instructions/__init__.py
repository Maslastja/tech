from flask import Blueprint, render_template
from . import views
from app.models.instructions import Instruction

bp = Blueprint('instructions', __name__, template_folder='templates',
               static_folder='static', static_url_path='/instructions/static')
options = {'url_prefix': '/instructions'}

bp.add_url_rule('/', view_func=views.start_page,
                methods=['GET', 'POST'])

bp.add_url_rule('/openins', view_func=views.open_ins, methods=['GET', 'POST'])

@bp.route('/ins=<id>')
def read_instr(id):
        ins = Instruction.get(id=id)
        return render_template('faqread.html', title='Инструкции',
                               ins = ins)

