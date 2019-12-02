from flask import render_template, request, flash, redirect, url_for, session
from datetime import datetime
from app.admin.forms import UserForm, TypesForm, LinkForm
from app.models.users import User
from app.models.links import Link
from app.models.news import News
from app.models.instructions import Instruction
from app.models.types import TypeLinks, TypeNews
from app.admin.func import find_all_users, find_all_types, find_all_links

#---------------------------------USERS----------------------------------------#
def get_users():
    users = find_all_users()
    resp = render_template('userslist.html', users=users, subname='users',
                           title='Список пользователей')
    if request.method == 'POST':
        if 'changesub' in request.form:
            dictform = dict(request.form)
            valuesub = dictform['changesub']
            resp = redirect(url_for('admin.open_user', id=valuesub))
        
        if 'delsub' in request.form:
            dictform = dict(request.form)
            valuesub = int(dictform['delsub'])
            for_del = check_for_del_user(valuesub)
            if for_del:
                result = User.delete_by_id(valuesub)
            resp = redirect(url_for('admin.get_users'))
        
        if 'adduser' in request.form:
            resp = redirect(url_for('admin.open_user'))
    
    return resp
    
def open_user():
    if 'back' in request.form:
        return redirect(url_for('admin.get_users'))
    
    arg_id = request.args.get('id')
    if arg_id is not None:
        user = User.get_by_id(arg_id)
        form = UserForm(request.form or None, obj=user)
        titleform = 'Изменить пользователя'
    else:
        form = UserForm(request.form or None)
        titleform = 'Добавить пользователя'
        
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            u = user
            u.username=form.username.data
            u.isadmin=form.isadmin.data,
            u.isactive=form.isactive.data
        else:    
            u = User(username=form.username.data,
                     pwd=form.password.data,
                     isadmin=form.isadmin.data,
                     isactive=form.isactive.data)
        u.save()
        return redirect(url_for('admin.get_users'))
    
    return render_template('elemform.html', form=form, title = titleform,
                           subname='users')

def check_for_del_user(user_id):
    sel1 = Link.select().where(Link.user_id == user_id).limit(1) 
    sel2 = News.select().where(News.user_id == user_id).limit(1)
    sel3 = Instruction.select().where(Instruction.user_id == user_id).limit(1)    
       
    check = True if (len(sel1)==0 and len(sel2)==0 and len(sel3)==0) else False
    return check

#---------------------------------TYPES----------------------------------------#
def get_types_news():
    resp = get_types('news')
    return resp

def get_types_links():
    resp = get_types('links')
    return resp

def get_types(tab):
    types = find_all_types(tab)
    resp = render_template('typelist.html', types=types, subname=f'type{tab}', 
                           title='Список типов')
    
    if request.method == 'POST':
        if 'changesub' in request.form:
            dictform = dict(request.form)
            valuesub = dictform['changesub']
            resp = redirect(url_for('admin.open_type', id=valuesub, tab=tab))
        
        if 'delsub' in request.form:
            table = TypeNews if tab == 'news' else TypeLinks
            dictform = dict(request.form)
            valuesub = int(dictform['delsub'])
            for_del = check_for_del(tab, valuesub)
            if for_del:
                result = table.delete_by_id(valuesub)           
            
            if tab == 'news':
                return redirect(url_for('admin.get_types_news'))
            else:
                return redirect(url_for('admin.get_types_links'))
        
        if 'addtype' in request.form:
            resp = redirect(url_for('admin.open_type', tab=tab))
    
    return resp

def check_for_del(tab, id):
    if tab == 'news':
            sel = News.select().where(News.typenews_id == id).limit(1)
    else:
            sel = Link.select().where(Link.typelink_id == id).limit(1)
    check = False if len(sel)>0 else True
    return check
    
def open_type():
    arg_tab = request.args.get('tab')
    if 'back' in request.form:
        if arg_tab == 'news':
            return redirect(url_for('admin.get_types_news'))
        else:
            return redirect(url_for('admin.get_types_links'))
    
    table = TypeNews if arg_tab == 'news' else TypeLinks
    arg_id = request.args.get('id')
    if arg_id is not None:
        t = table.get_by_id(arg_id)
        form = TypesForm(request.form or None, obj=t)
        titleform = 'Изменить тип'
    else:
        form = TypesForm(request.form or None)
        titleform = 'Добавить тип'
        
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            result = (table
                      .update(typename=form.typename.data,
                              typecode=form.typecode.data,
                              isactive=form.isactive.data
                              )
                      .where(table.id==arg_id)
                      .execute())
        else:
            t = table(typename=form.typename.data,
                      typecode=form.typecode.data,
                      isactive=form.isactive.data)
            t.save()
        
        if arg_tab == 'news':
            return redirect(url_for('admin.get_types_news'))
        else:
            return redirect(url_for('admin.get_types_links'))
    
    return render_template('elemform.html', form=form, title = titleform,
                           subname=f'type{arg_tab}')

#----------------------------------LINKS---------------------------------------#
def get_links():
    links = find_all_links()
    resp = render_template('linkslist.html', links=links, subname='links', 
                           title='Список ссылок')
    if request.method == 'POST':
        if 'changesub' in request.form:
            dictform = dict(request.form)
            valuesub = dictform['changesub']
            resp = redirect(url_for('admin.open_link', id=valuesub))
        
        if 'delsub' in request.form:
            dictform = dict(request.form)
            valuesub = int(dictform['delsub'])
            result = Link.delete_by_id(valuesub)
            return redirect(url_for('admin.get_links'))
        
        if 'addlink' in request.form:
            resp = redirect(url_for('admin.open_link'))
    
    return resp

def open_link():
    if 'back' in request.form:
        return redirect(url_for('admin.get_links'))
    
    arg_id = request.args.get('id')
    if arg_id is not None:
        link = Link.get_by_id(arg_id)
        form = LinkForm(request.form or None, obj=link)
        titleform = 'Изменить ссылку'
    else:
        form = LinkForm(request.form or None)
        titleform = 'Добавить ссылку'
        
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            l = link
            l.linkname=form.linkname.data
            l.fullname=form.fullname.data
            l.typelink=form.typelink.data
            l.changedate=datetime.today()
            l.user=session.user['user_id']
        else:
            d = datetime.today()
            l = Link(linkname=form.linkname.data,
                     fullname=form.fullname.data,
                     typelink=form.typelink.data,
                     createdate=d,
                     changedate=d,
                     user=session.user['user_id'])
        l.save()
        return redirect(url_for('admin.get_links'))
    
    return render_template('elemform.html', form=form, title = titleform,
                           subname='links')
