from flask import (render_template, request, redirect,
                   url_for, session, jsonify)
import requests
from app.admin.forms import PhoneForm
from app.models.phones import Phones

types = {
    'amb': 'Амбулаторный',
    'hosp': 'Стационар',
    'dhosp': 'Дневной стационар',
    'reanim': 'Реанимация',
    'oper': 'Операционный блок',
    'serv': 'Вспомогательные службы',
    'nonmed': 'Немедицинский'
    }


def get_filials():
    filials = requests.get('http://struc.iood.ru/api/branch')
    filials = filials.json()
    fil = {}
    for el in filials:
        fil[el['id']] = el['name']
    return fil


def get_otdels(valfil):
    otdels = requests.get(f'http://struc.iood.ru/api/branch/{valfil}/'
                          'deps?types=hosp,dhosp,amb,reanim,oper,serv,nonmed')
    otdels = otdels.json()
    otd = {}
    # print(otdels)
    for el in otdels:
        otd[el['id']] = el['name']
    return otd


def get_phones():
    idotd = request.args.get('idotd')
    searchph = request.args.get('searchph')
    valfil = request.args.get('valfil')
    if searchph:
        otdels = get_otdels(valfil)
        searchph = searchph.lower()
        searchph = searchph.split()
    sel = Phones.select(Phones.id,
                        Phones.idotd,
                        Phones.isgeneral,
                        Phones.isactive,
                        Phones.comment,
                        Phones.nameabon,
                        Phones.numberin,
                        Phones.numberout,
                        Phones.email)
    if session.user and 'SYS' in session.user.roles:
        if idotd:
            sel = sel.where((Phones.idotd == idotd) & (Phones.idfil == valfil))
    else:
        if idotd:
            sel = sel.where((Phones.isactive == 1) &
                            (Phones.idotd == idotd) &
                            (Phones.idfil == valfil))
        else:
            sel = sel.where((Phones.isactive == 1) & (Phones.idfil == valfil))
    sel = (sel
           .order_by(Phones.comment,
                     Phones.isgeneral.desc(),
                     Phones.nameabon)
           .namedtuples())

    phones = []
    for el in sel:
        if searchph:
            add = True
            for s in searchph:
                if (el.comment is None or el.comment is not None and
                        el.comment.lower().find(s) == -1):
                    add = False
            if add:
                elotd = otdels[el.idotd] if otdels.get(el.idotd) else ''
                elnumbout = el.numberout if el.numberout else ''
                phones.append({'id': el.id,
                               'isgeneral': el.isgeneral,
                               'isactive': el.isactive,
                               'comment': el.comment if el.comment else '',
                               'otdel': elotd,
                               'idotdel': el.idotd if el.idotd else '',
                               'nameabon': el.nameabon,
                               'numberin': el.numberin if el.numberin else '',
                               'numberout': elnumbout,
                               'email': el.email if el.email else ''})
        else:
            phones.append({'id': el.id,
                           'isgeneral': el.isgeneral,
                           'isactive': el.isactive,
                           'comment': el.comment if el.comment else '',
                           'nameabon': el.nameabon,
                           'numberin': el.numberin if el.numberin else '',
                           'numberout': el.numberout if el.numberout else '',
                           'email': el.email if el.email else ''})
#    print(phones)

    return jsonify(phones)


def phonesnew():
    fil = get_filials()

    resp = render_template('phonesnew.html', title='Телефонный справочник',
                           fil=fil, types=types)
    if request.method == 'POST':
        if 'changesub' in request.form:
            valuesub = request.form['changesub']
            resp = redirect(url_for('phonebook.open_phone', id=valuesub))

        if 'delsub' in request.form:
            valuesub = int(request.form['delsub'])
            (Phones
             .update(isactive=False)
             .where(Phones.id == valuesub)
             .execute())
            resp = redirect(url_for('phonebook.phonesnew'))

        if 'addsub' in request.form:
            resp = redirect(url_for('phonebook.open_phone'))

    return resp


def get_otd_by_id(idotd):
    strres = f'http://struc.iood.ru/api/dep/{idotd}?fields=id,name'
    otd = requests.get(strres)
    otd = otd.json()
    return otd['name'] if 'name' in otd else ''


def open_phone():
    if 'back' in request.form:
        return redirect(url_for('phonebook.phonesnew'))

    arg_id = request.args.get('id')
    fil = get_filials()

    if arg_id is not None:
        ph = Phones.get_by_id(arg_id)
        form = PhoneForm(request.form or None, obj=ph)
        titleform = 'Изменить номер'
        nameotd = get_otd_by_id(ph.idotd)
        form.otd.choices = [(ph.idotd, nameotd)]
    else:
        form = PhoneForm(request.form or None)
        titleform = 'Добавить номер'
        form.otd.choices = [('', '')]

    form.fil.choices = [(f, fil[f]) for f in fil]
    form.typeotd.choices = [('', 'все')]+[(t, types[t]) for t in types]

    if request.method == 'POST':
        # т.к. список был динамически изменен выборку принудительно подзаменяем
        # на выбранный элемент в форме
        if form.otd.data:
            nameotd = get_otd_by_id(form.otd.data)
            form.otd.choices = [(form.otd.data, nameotd)]
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            (Phones
             .update(idfil=form.fil.data,
                     idotd=form.otd.data,
                     typeotd=form.typeotd.data,
                     nameabon=form.nameabon.data,
                     numberin=form.numberin.data,
                     numberout=form.numberout.data,
                     comment=form.comment.data,
                     email=form.email.data,
                     isgeneral=form.isgeneral.data,
                     isactive=form.isactive.data)
             .where(Phones.id == arg_id)
             .execute())
        else:
            ph = Phones(idfil=form.fil.data,
                        idotd=form.otd.data,
                        typeotd=form.typeotd.data,
                        nameabon=form.nameabon.data,
                        numberin=form.numberin.data,
                        numberout=form.numberout.data,
                        comment=form.comment.data,
                        email=form.email.data,
                        isgeneral=form.isgeneral.data,
                        isactive=form.isactive.data)
            ph.save()
        return redirect(url_for('phonebook.phonesnew'))

    return render_template('phoneform.html', title=titleform,
                           form=form)
