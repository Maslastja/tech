import os
import pytest
import requests
import tempfile
from flask import Flask
from config.database import db, Collect
from app.models import all_models
from app.utils import register_bp
from app.auth import MySessionInterface


typesl = {1: 'ссылки ИООД',
          2: 'ссылки Здравоохранение',
          3: 'дополнительные ссылки',
          4: 'файлы',
          5: 'видеоматериалы'}
typesn = {1: 'news',
          2: 'conf',
          3: 'spec'}


@pytest.fixture(scope='session')
def temp():
    yield tempfile.NamedTemporaryFile()


@pytest.fixture(scope='session')
def client(temp):
    app = Flask('app', root_path=os.getcwd(),
                static_folder='static',
                template_folder='app/templates')
    app.config.from_object('config.settings_test')
    app.config['DATABASE_URL'] = f'sqliteext:///{temp.name}'
    db.init_app(app)
    db.database.aggregate('collect')(Collect)
    db.database.create_tables(all_models())
    for mod in all_models():
        if (mod.__name__ == 'TypeLinks' and
           mod.select().count() == 0):
            for t in typesl:
                mod.insert(typename=typesl.get(t), typecode=t).execute()
        if (mod.__name__ == 'TypeNews' and mod.select().count() == 0):
            for t in typesn:
                mod.insert(typename=typesn.get(t), typecode=t).execute()
    register_bp(app)
    app.session_interface = MySessionInterface()

    with app.test_client() as client:
        ses = requests.post(os.environ['AUTH'],
                            data={'login': os.environ['LOGIN'],
                                  'password': os.environ['PASSWORD']})
        client.set_cookie('tech.iood.ru', 'sid', value=ses.cookies['sid'])
        yield client
