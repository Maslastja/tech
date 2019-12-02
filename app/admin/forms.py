from wtforms import (Form, widgets, StringField, SelectField, BooleanField, 
                     PasswordField)
from wtforms.validators import ValidationError, DataRequired
from wtfpeewee.orm import model_form, ModelConverter 
from app.models.users import User
from app.models.types import TypeLinks, TypeNews
from app.models.links import Link
from app.models.news import News
from app.models.instructions import Instruction


#def validate_username():
    #user = User.select().where(User.username == username.data)
    #if len(user) != 0:
        #raise ValidationError('Такой пользователь уже существует. '
                                #'Введите другое имя пользователя')        
UserForm = model_form(User, field_args=
                      {'username': dict(label='логин',
                                   validators=[DataRequired('значение не заполнено')]),
                       'password': dict(label='пароль', 
                                   widget = widgets.PasswordInput(),
                                   validators=[DataRequired('значение не заполнено')]),
                       'isadmin': dict(label='администратор'),
                       'isactive': dict(label='активный')})

TypesForm = model_form(TypeLinks, field_args=
                           {'typename': dict(label='тип',
                                   validators=[DataRequired('значение не заполнено')]),
                            'typecode': dict(label='код типа',
                                    validators=[DataRequired('значение не заполнено')]),
                            'isactive': dict(label='активный')
                            })

LinkForm = model_form(Link, exclude=('user', 'createdate', 'changedate'), 
                      field_args=
                      {'linkname': dict(label='наименование',
                                   validators=[DataRequired('значение не заполнено')]),
                       'fullname': dict(label='полный адрес', 
                                   validators=[DataRequired('значение не заполнено')]),
                       'typelink': dict(label='тип ссылки',
                                        widget = widgets.Select())})

NewsForm = model_form(News, exclude=('text', 'user','createdate', 'changedate'), 
                      field_args=
                      {'name': dict(label='заголовок новости',
                                        validators=[DataRequired('значение не заполнено')]),
                       'typenews': dict(label='тип новости',
                                        widget = widgets.Select())})

InstructionForm = model_form(Instruction, exclude=('text', 'user','createdate',
                                                   'changedate'), 
                             field_args=
                             {'name': dict(label='заголовок инструкции',
                                        validators=[DataRequired('значение не заполнено')])})

    
