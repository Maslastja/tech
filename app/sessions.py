import secrets
from flask import request
from flask.sessions import SessionInterface, SessionMixin
from datetime import datetime
from werkzeug.datastructures import CallbackDict
from app.models.sessions import SessionsStore

class MyDatabaseSession(CallbackDict, SessionMixin):
    def exist_session(self):
        sid = self.sid
        s = SessionsStore.get_or_none(SessionsStore.token == sid)
        return s
    
    def save_in_db(self,user):
        if self.user:
            result = (SessionsStore.insert(
                         token = self.sid,
                         user = self.user['user_id'],
                         DateCreate = datetime.today(),
                         DateLastReq = datetime.today()
                         ).execute())
    
    def delete_session(self):
        result = (SessionsStore.delete()
                  .where(SessionsStore.token == self.sid)
                  .execute())
        self.clear()
        
    def change_last_req(self):
        s = SessionsStore.get(SessionsStore.token == self.sid)
        s.DateLastReq = datetime.today()
        s.save()
    
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False
        self.accessed = False
        self.user = None
        self.sid = None
    
            
class MyDatabaseSessionInterface(SessionInterface):
    session_class = MyDatabaseSession
    
    def open_session(self, app, request):
        if request.endpoint == 'static':
            return None
        
        sid = request.cookies.get(app.session_cookie_name)
        s = self.session_class()
        if not sid:
            sid = secrets.token_hex(24)
            s.sid = sid
        
        sbd = SessionsStore.get_or_none(SessionsStore.token == sid)
        s.sid = sid
        if sbd:
            user = {
                    'user_id': sbd.user.id,
                    'username': sbd.user.username,
                    'isadmin': sbd.user.isadmin,
                }
            s.user = user
        return s
            
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        
        s = session.exist_session()
        if not s:
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
                return
        
        sid = request.cookies.get(app.session_cookie_name)
        #if sid is None: #тоже вариант
        if session.user and sid != session.sid:
            httponly = self.get_cookie_httponly(app)
            secure = self.get_cookie_secure(app)
            response.set_cookie(app.session_cookie_name, session.sid,
                                httponly=httponly, domain=domain, 
                                path=path, secure=secure)
 
 