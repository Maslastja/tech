from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from app.admin.forms import TypesForm, LinkForm
from app.models.links import Link
from app.models.news import News
from app.models.types import TypeLinks, TypeNews
from app.admin.func import find_all_types, links_ajax


# ---------------------------------TYPES------------------------------------- #
def get_types_news():
    return get_types('news')


def get_types_links():
    return get_types('links')


def get_types(tab):
    types = find_all_types(tab)

    if request.method == 'POST':
        if 'changesub' in request.form:
            valuesub = request.form['changesub']
            url = url_for('admin.open_type', id=valuesub, tab=tab)

        if 'delsub' in request.form:
            table = TypeNews if tab == 'news' else TypeLinks
            valuesub = int(request.form['delsub'])
            table.update(isactive=False).where(table.id == valuesub).execute()
            # for_del = check_for_del(tab, valuesub)
            # if for_del:
            # result = table.delete_by_id(valuesub)
            if tab == 'news':
                url = url_for('admin.get_types_news')
            else:
                url = url_for('admin.get_types_links')

        if 'addtype' in request.form:
            url = url_for('admin.open_type', tab=tab)

        return redirect(url)

    return render_template('typelist.html', types=types, subname=f'type{tab}',
                           title='Список типов')


def check_for_del(tab, id):
    if tab == 'news':
        sel = News.select().where(News.typenews_id == id).limit(1)
    else:
        sel = Link.select().where(Link.typelink_id == id).limit(1)
    check = False if len(sel) > 0 else True
    return check


def open_type():
    arg_tab = request.args.get('tab')
    if 'back' in request.form:
        if arg_tab == 'news':
            return redirect(url_for('admin.get_types_news'))
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
            table.update(
                typename=form.typename.data,
                typecode=form.typecode.data,
                isactive=form.isactive.data
            ).where(table.id == arg_id).execute()
        else:
            t = table(typename=form.typename.data,
                      typecode=form.typecode.data,
                      isactive=form.isactive.data)
            t.save()

        if arg_tab == 'news':
            return redirect(url_for('admin.get_types_news'))
        return redirect(url_for('admin.get_types_links'))

    return render_template('elemform.html', form=form, title=titleform,
                           subname=f'type{arg_tab}')


# ----------------------------------LINKS------------------------------------ #
def get_links_ajax():
    typelink = request.args.get('typelink')
    return links_ajax(typelink)


def get_links():
    types = find_all_types('links')
    typeslinks = {}
    for el in types:
        typeslinks[el['id']] = el['typename']

    if request.method == 'POST':
        dictform = dict(request.form)        if 'changesub' in request.form:
            valuesub = dictform['changesub']
            url = url_for('admin.open_link', id=valuesub)

        if 'delsub' in request.form:
            valuesub = int(dictform['delsub'])
            Link.update(isactive=False).where(Link.id == valuesub).execute()
            # result = Link.delete_by_id(valuesub)
            url = url_for('admin.get_links')

        if 'addlink' in request.form:
            url = url_for('admin.open_link')

        return redirect(url)

    return render_template('linkslist.html', subname='links',
                           title='Список ссылок', types=typeslinks)


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
            link.linkname = form.linkname.data
            link.fullname = form.fullname.data
            link.typelink = form.typelink.data
            link.isactive = form.isactive.data
            link.changedate = datetime.today()
            link.user = session.user.id
            link.save()
        else:
            d = datetime.today()
            elem = Link(linkname=form.linkname.data,
                        fullname=form.fullname.data,
                        typelink=form.typelink.data,
                        isactive=form.isactive.data,
                        createdate=d,
                        changedate=d,
                        user=session.user.id)
            elem.save()
        return redirect(url_for('admin.get_links'))

    return render_template('elemform.html', form=form, title=titleform,
                           subname='links')
