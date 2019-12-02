from flask import request, render_template, redirect, session
from .forms import LoginForm
from app.utils import login_required
from app.models.users import User

def login():
    form = LoginForm(request.form or None)
    if 'back' in request.form:
        return redirect('/')
    if request.method == 'POST' and form.validate():
        resp = redirect('/')
            
        #попытка получить и записать пользователя в сессию
        username = form.username.data
        user_bd = (User.select()
                .where(User.username == username).get())
        user = {
                'user_id': user_bd.id,
                'username': user_bd.username,
                'isadmin': user_bd.isadmin,
            }
        session.user = user
        session.save_in_db(user)
        return resp
            
    resp = render_template('login.html', form=form, title='Вход')
    
    return resp

@login_required
def logout():
    #удалить информацию о сессии из бд
    session.delete_session()
    session.clear()
    resp = redirect('/')
    
    return resp

