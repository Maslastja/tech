import os

DATABASE = os.getenv('DATABASE_URL')
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = 'sid'
LOGIN_URL = 'http://auth.iood.ru/user/login?next={}'
SESSION_GET = 'http://auth.iood.ru/sess/get'
SESSION_STORE = 'http://auth.iood.ru/sess/update'

PHONE_IRK = 'smb://192.168.109.20/Common Linux/ATC/телефоны 2019.ods'
PHONE_ANG = 'smb://192.168.109.20/Common Linux/ATC/телефоны Ангарска.xls'
PHONE_BR = 'smb://192.168.109.20/Common Linux/ATC/телефоны Братск1.xls'
