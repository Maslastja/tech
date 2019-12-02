from wtforms import (Form, StringField, PasswordField, 
                     BooleanField, validators)
from werkzeug.security import check_password_hash
from app.models.users import User

class LoginForm(Form):
    username = StringField('Логин', 
                           [validators.DataRequired('поле не заполнено')])
    password = PasswordField('Пароль',
                             [validators.DataRequired('поле не заполнено')])

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        user = User.select().where(User.username == self.username.data)
        if len(user) == 0:
            self.username.errors=('Неверный логин',)
            return False
        else:
            usr = user.get()
            if not usr.check_password(self.password.data):
                self.password.errors=('Неверный пароль',)
                return False
            else:
                return True
    
        
