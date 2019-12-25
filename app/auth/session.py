from flask import json
from flask.sessions import SessionMixin

from collections import namedtuple
from werkzeug.datastructures import CallbackDict

import requests


def make_resp(app, sid, method, url, **kwargs):
    data = {}
    kwargs['headers'] = kwargs.pop('headers', {})
    kwargs['headers']['X-Requested-With'] = 'XMLHttpRequest'
    kwargs['cookies'] = {'app': app.name, app.session_cookie_name: sid}
    kwargs['timeout'] = 10

    try:
        r = requests.request(method, url, **kwargs)
    # except: # замена неявного исключения
    except requests.RequestException:
        app.logger.error('Failed to connect to session store')
    else:
        try:
            data = r.json()
        except ValueError:
            app.logger.error('Error processing session data {}'.format(r.text))
        else:
            if not r.ok:
                app.logger.warn('Error in session data: {}'.format(data))
    # print(data)
    return data


class Session(CallbackDict, SessionMixin):

    def __init__(self, sid=None, initial={}):
        def on_update(self):
            self.modified = True

        user_data = initial.get('user')
        if user_data:
            User = namedtuple('User', user_data.keys())
            self.user = User(**user_data)
            self.user_fullname = ' '.join((self.user.family,
                                           self.user.name,
                                           self.user.patr))
        else:
            self.user = None

        self.sid = sid
        self.branch = initial.get('branch')
        self.client = initial.get('client')
        self.modified = False

        CallbackDict.__init__(self, initial.get('data'), on_update)

    @classmethod
    def find(cls, app, sid):
        data = make_resp(app, sid, 'get', app.config['SESSION_GET'])
        return cls(sid, data)

    def save(self, app):
        make_resp(app, self.sid, 'post', app.config['SESSION_STORE'],
                  data=json.dumps(self, encoding='utf-8'),
                  headers={'Accept': 'text/plain',
                           'Content-type': 'application/json'})
