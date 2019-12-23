from flask import current_app
import urllib.request
from smb.SMBHandler import SMBHandler
from odf.opendocument import load
from odf.table import TableRow, TableColumn, TableCell


def get_tnumb(rows, i, col):
    tnumb = []
    while i <= len(rows)-1:
        if i == len(rows)-1:
            return [tnumb, i]
        i = i+1
        row = rows[i]
        cells = row.getElementsByType(TableCell)
        if len(cells) >= col+3:
            if str(cells[col+1]) == '' and str(cells[col+2]) == '':
                return [tnumb, i]
            tnumb.append({'name': str(cells[col]),
                          'tsokr': str(cells[col+1]),
                          'tgorod': str(cells[col+2])})


def pars_phone():
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(current_app.config['PHONE_IRK'])
    doc = load(fh)
    fh.close()
    rows = doc.getElementsByType(TableRow)
    columns = doc.getElementsByType(TableColumn)

    numbers = []
    numbersotd = []
    col = 0
    while col <= len(columns):
        i = 1
        while i <= len(rows)-1:
            row = rows[i]
            cells = row.getElementsByType(TableCell)
            if len(cells) >= col+3:
                if str(cells[col+1]) == '' and str(cells[col+2]) == '':
                    if str(cells[col]) != '':
                        tnumb = get_tnumb(rows, i, col)
                        i = tnumb[1]
                        numbersotd.append({'name': str(cells[col]),
                                           'tnumb': tnumb[0]})
                    else:
                        i = i+1
                else:
                    numbers.append({'name': str(cells[col]),
                                    'tsokr': str(cells[col+1]),
                                    'tgorod': str(cells[col+2])})
                    i = i+1
            else:
                i = i+1
        col = col+3
    return [numbers, numbersotd]
