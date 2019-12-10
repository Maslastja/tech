from wtforms import (Form, widgets, StringField, SelectField, BooleanField, 
                     PasswordField)
from wtforms.validators import ValidationError, DataRequired
from wtfpeewee.orm import model_form, ModelConverter, WPDateField
from datetime import datetime
from app.models.users import User
from app.models.types import TypeLinks, TypeNews
from app.models.links import Link
from app.models.news import News
from app.models.instructions import Instruction
from app.models.calendar import Calendar


def validate_username(form, field):
    #print(field.object_data)  #начальное значениеи поля
    #print(field.data)         #текущее значение поля
    if field.object_data != field.data:
    #raise
        user = User.get_or_none(User.username == field.data)
        if user:
            raise ValidationError('Такой пользователь уже существует. '
                                    'Введите другое имя пользователя')   

def validate_time(form, field):
    #print(field.object_data)  #начальное значениеи поля
    #print(field.data)         #текущее значение поля
    d = form.day.data.strftime('%Y-%m-%d')
    sel = Calendar.select().where(Calendar.day == d)
    for ev in sel:
        if ((field.name == 'timestart' and field.object_data != field.data and
            field.data >= ev.timestart and field.data < ev.timeend) or
           (field.name == 'timeend' and field.object_data != field.data and 
            field.data > ev.timestart and field.data <= ev.timeend)):
            raise ValidationError('Указанное время занято')   
    
UserForm = model_form(User, field_args=
                      {'username': dict(label='логин',
                                   validators=[DataRequired('значение не заполнено'),
                                               validate_username]),
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

NewsForm = model_form(News, exclude=('user','createdate', 'changedate'), 
                      field_args=
                      {'name': dict(label='заголовок новости',
                                        validators=[DataRequired('значение не заполнено')]),
                       'typenews': dict(label='тип новости',
                                        widget = widgets.Select()),
                       'text': dict(label='текст записи', id='redactor',
                                validators=[DataRequired('значение не заполнено')])})

InstructionForm = model_form(Instruction, exclude=('user','createdate',
                                                   'changedate'), 
                             field_args=
                             {'name': dict(label='заголовок инструкции',
                                        validators=[DataRequired('значение не заполнено')]),
                              'text': dict(label='текст инструкции', 
                                           id='redactor',
                                           validators=[DataRequired('значение не заполнено')])
                              })

CalendarForm = model_form(Calendar,  
                      field_args=
                      {'day': dict(label='день',
                                   render_kw= dict(type='date'),
                                   validators=[DataRequired('значение не заполнено')]),
                       'timestart': dict(label='с',
                                   render_kw= dict(type='time'),
                                   validators=[DataRequired('значение не заполнено'),
                                               validate_time]),
                       'timeend': dict(label='по',
                                 render_kw= dict(type='time'),
                                 validators=[DataRequired('значение не заполнено'),
                                             validate_time]),
                       'event': dict(label='мероприятие', 
                                   validators=[DataRequired('значение не заполнено')]),
                       'resp': dict(label='ответственный'),
                       'comment': dict(label='комментарий')
                       })
