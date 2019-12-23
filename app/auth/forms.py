from wtforms import Form, StringField, PasswordField
# from app.models.users import User


class LoginForm(Form):
    login = StringField('Логин', render_kw={'autocomplete': 'off'})
    password = PasswordField('Пароль')
