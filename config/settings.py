import os

DATABASE = 'sqliteext:///db_techpage.sqlite'
DATABASE_URL = 'sqliteext:///db_techpage.sqlite'
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = 'sid'
LOGIN_URL = 'http://auth.iood.ru/user/login?next={}'
SESSION_GET = 'http://auth.iood.ru/sess/get'
SESSION_STORE = 'http://auth.iood.ru/sess/update'
