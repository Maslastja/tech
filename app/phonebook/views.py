from flask import (render_template, request, Response, current_app, redirect,
                   url_for, session)
import requests
import urllib.request
import json
from smb.SMBHandler import SMBHandler
from app.phonebook.func import pars_phone
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


# def phones():
    # phones = pars_phone()
    # print(phones[1])
    # for el in phones[0]:
    # ph = Phones(idfil='irk',
    # idotd='irk.nonmed.54',
    # typeotd='nonmed',
    # nameabon=el['name'],
    # numberin=el['tsokr'],
    # numberout=el['tgorod'],
    # isactive=True)
    # ph.save()
    # for otd in phones[1]:
    # for el in otd['tnumb']:
    # ph = Phones(idfil='irk',
    # idotd='irk.nonmed.54',
    # typeotd='nonmed',
    # comment=otd['name'],
    # nameabon=el['name'],
    # numberin=el['tsokr'],
    # numberout=el['tgorod'],
    # isactive=True)
    # ph.save()

    # return render_template('phones.html', phones=phones[0],
                           # phonesotd=phones[1])


# def load_phones():
    # type_ph = request.args.get('type_phone')

    # director = urllib.request.build_opener(SMBHandler)
    # if type_ph == 'irk':
        # doc = director.open(current_app.config['PHONE_IRK'])
        # return Response(
            # doc,
            # mimetype='spreadsheet/ods',
            # headers={'Content-disposition':
                     # 'attachment; filename=phones.ods'})

    # if type_ph == 'ang':
        # doc = director.open(current_app.config['PHONE_ANG'])
    # else:
        # doc = director.open(current_app.config['PHONE_BR'])

    # return Response(doc,
                    # mimetype='application/vnd.ms-excel',
                    # headers={'Content-disposition':
                             # 'attachment; filename=phones.xls'})


def get_filials():
    filials = requests.get('http://struc.iood.ru/api/branch')
    filials = filials.json()
    fil = {}
    for el in filials:
        fil[el['id']] = el['name']
    return fil


def get_phones():
    idotd = request.args.get('idotd')
    sel = Phones.select(Phones.id,
                        Phones.isgeneral,
                        Phones.isactive,
                        Phones.comment,
                        Phones.nameabon,
                        Phones.numberin,
                        Phones.numberout,
                        Phones.email)
    if session.user and 'SYS' in session.user.roles:
        if idotd:
            sel = sel.where(Phones.idotd == idotd)
    else:
        if idotd:
            sel = sel.where((Phones.isactive == 1) &
                            (Phones.idotd == idotd))
        else:
            sel = sel.where(Phones.isactive == 1)
    sel = (sel
           .order_by(Phones.comment,
                     Phones.isgeneral.desc(),
                     Phones.nameabon)
           .namedtuples())

    phones = []
    for el in sel:
        phones.append({'id': el.id,
                       'isgeneral': el.isgeneral,
                       'isactive': el.isactive,
                       'comment': el.comment if el.comment else '',
                       'nameabon': el.nameabon,
                       'numberin': el.numberin if el.numberin else '',
                       'numberout': el.numberout if el.numberout else '',
                       'email': el.email if el.email else ''})
    ff = json.dumps(phones)

    return ff


def phonesnew():
    fil = get_filials()

    resp = render_template('phonesnew.html', title='телефонный справочник',
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
    form.typeotd.choices = [(t, types[t]) for t in types]

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
