from flask import render_template, request, Response, current_app
import urllib.request
from smb.SMBHandler import SMBHandler
from app.phonebook.func import pars_phone


def phones():
    phones = pars_phone()
    return render_template('phones.html', phones=phones[0],
                           phonesotd=phones[1])


def load_phones():
    type_ph = request.args.get('type_phone')

    director = urllib.request.build_opener(SMBHandler)
    if type_ph == 'irk':
        doc = director.open(current_app.config['PHONE_IRK'])
        return Response(
            doc,
            mimetype='spreadsheet/ods',
            headers={'Content-disposition':
                     'attachment; filename=phones.ods'})

    if type_ph == 'ang':
        doc = director.open(current_app.config['PHONE_ANG'])
    else:
        doc = director.open(current_app.config['PHONE_BR'])

    return Response(doc,
                    mimetype='application/vnd.ms-excel',
                    headers={'Content-disposition':
                             'attachment; filename=phones.xls'})
