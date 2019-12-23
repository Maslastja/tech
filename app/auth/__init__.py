from flask.sessions import SessionInterface
from flask import Blueprint, render_template

from .session import Session
from .forms import LoginForm


class MySessionInterface(SessionInterface):

    def open_session(self, app, request):
        bp = request.blueprint or request.endpoint
        if bp in ('static',):
            return Session()

        sid = request.cookies.get(app.session_cookie_name, 'sid')
        return Session.find(app, sid)

    def save_session(self, app, session, response):
        if session.modified:
            session.save(app)


bp = Blueprint('auth', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', form=LoginForm(), title='Вход')
