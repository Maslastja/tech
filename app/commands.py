import click
import app.models as models
from flask.cli import AppGroup
from config.database import db

dbase = AppGroup('dbase')
# по умолчанию добавить значения
types = {1: 'ссылки ИООД',
         2: 'ссылки Здравоохранение',
         3: 'дополнительные ссылки',
         4: 'файлы',
         5: 'видеоматериалы'}


@dbase.command()
def create_all_tabs():
    """Creating tables in database by all models in app"""
    ArModels = models.all_models()
    print(ArModels)
    db.database.create_tables(ArModels)
    for mod in ArModels:
        if (mod.__name__ == 'TypeLinks' and
           mod.select().count() == 0):
            for t in types:
                mod.insert(typename=types.get(t), typecode=t).execute()


@dbase.command()
@click.argument('name')
def create_table(name):
    """Create table in database"""
    mod = models.one_model(name)
    if mod is not None:
        mod.create_table()
        if (name == 'TypeLinks' and
           mod.select().count() == 0):
            for t in types:
                mod.insert(typename=types.get(t), typecode=t).execute()
    else:
        print('таблица не существует')


@dbase.command()
@click.argument('login')
def create_admin(login):
    create_user_in_db(login, True)


@dbase.command()
@click.argument('login')
def create_user(login):
    create_user_in_db(login, False)


def create_user_in_db(login, isadmin):
    password = click.prompt('Задайте пароль', hide_input=True)
    confirm = click.prompt('Подтвердите пароль', hide_input=True)
    if password != confirm:
        raise click.BadParameter('Пароль не совпадает')
    u = models.User(username=login,
                    pwd=password,
                    isadmin=isadmin)
    u.save()
    str_isadmin = 'администратор' if isadmin else 'пользователь'
    click.echo(f'Создан {str_isadmin}: {login}')
