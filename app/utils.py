import os
import importlib
from logging.handlers import RotatingFileHandler
from peewee import logging
from flask import session, redirect
from functools import wraps

import urllib.request
from smb.SMBHandler import SMBHandler
from odf.opendocument import load
from odf.table import TableRow, TableColumn, TableCell
from odf.text import P
from odf.style import Style, StyleElement, TableCellProperties

def logapp(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', 
                                        maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: '
    '%(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('techpage app')

def register_bp(app):
    #print(app.import_name)
    #возможно можно использовать import_name т.к. это название папки 
    #приложения, в которой находятся все дополнительные папки и файлы
    
    for address, dirs, files in os.walk(f'{app.import_name}'):
        for d in dirs:
            try:
                #print(f'ADR {address}.{d}')
                module = importlib.import_module(f'{address}.{d}')
                if hasattr(module, 'bp'):
                    bp = module.bp
                    opt = {}
                    if hasattr(module, 'options'):
                        opt = module.options
                        
                    app.register_blueprint(bp, **opt)
            except (ImportError, TypeError) as e:
                #app.logger.exception(e)
                #print(f'{address}.{d}')
                #if d == 'schedule':
                    #module = importlib.import_module(f'{address}.{d}')
                continue


#декоратор ограничения использования функций только авториз. пользователей
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.user:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

##формат времени для шаблонов jinja2
#def format_datetime(value, format="%d.%m.%Y %H:%M"):
    #if value is None:
        #return ""
    #return value.strftime(format)



def get_tnumb(rows, i, col):
    tnumb = []
    while i <= len(rows)-1:
        #print(len(rows))
        if i == len(rows)-1:
            return [tnumb, i]
        i=i+1
        row = rows[i]
       # print(i)
        cells = row.getElementsByType(TableCell)
        if len(cells) >= col+3:
            if str(cells[col+1]) == '' and str(cells[col+2]) == '':
                return [tnumb, i]
            tnumb.append({'name': str(cells[col]),
                            'tsokr': str(cells[col+1]),
                            'tgorod': str(cells[col+2])})
         
def pars_phone():
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(os.getenv('PHONE_IRK'))
    #doc = load('/home/Maslastja/Документы/телефоны 2019.ods')
    doc = load(fh)
    fh.close()
    rows = doc.getElementsByType(TableRow)
    columns = doc.getElementsByType(TableColumn)
    
    countcol = len(columns)//3
    #row=rows[53]
    #cells = row.getElementsByType(TableCell)
    #print(str(cells[5]))
    numbers = []
    numbersotd = []
    col = 0
    while col <= len(columns):
    #for col in range(0, len(columns)):
        i=1
        while i <= len(rows)-1:
            #print(f'kol {col} str {i}')
            row = rows[i]
            cells = row.getElementsByType(TableCell)
            #print(len(cells))
            #print(cells[col+1])
            #print(cells[col+2])
            if len(cells) >= col+3:
                if str(cells[col+1]) == '' and str(cells[col+2]) == '':
                    if str(cells[col]) != '':
                        tnumb = get_tnumb(rows, i, col)
                        i = tnumb[1]
                        #print(f'new {i}')
                        #print(tnumb[0])
                        numbersotd.append({'name': str(cells[col]),
                                        'tnumb': tnumb[0]})
                    else:
                        i=i+1
                else:
                    numbers.append({'name': str(cells[col]),
                                    'tsokr': str(cells[col+1]),
                                    'tgorod': str(cells[col+2])})
                    i=i+1
            else:
                i=i+1
        col = col+3
    return [numbers, numbersotd]

