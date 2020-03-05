from app.core import create_app

app = create_app()
if app.debug:
    from app.commands import dbase
    app.cli.add_command(dbase)

if __name__ == '__main__':
    app.run(host='tech.iood.ru')
