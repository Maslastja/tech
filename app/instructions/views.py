from flask import render_template, redirect, url_for, request, session
from datetime import datetime
from app.admin.forms import InstructionForm
from app.models.instructions import Instruction


def get_instr():
    sel = Instruction.select()
    if not (session.user and 'SYS' in session.user.roles):
        sel = sel.where(Instruction.isactive == 1)
    ins = list(sel)
    return ins


def start_page():
    insall = get_instr()

    resp = render_template('faqlist.html', title='Инструкции',
                           insall=insall)
    if request.method == 'POST':
        if 'changeins' in request.form:
            valuesub = request.form['changeins']
            resp = redirect(url_for('instructions.open_ins', id=valuesub))

        if 'delins' in request.form:
            valuesub = int(request.form['delins'])
            (Instruction
             .update(isactive=False)
             .where(Instruction.id == valuesub)
             .execute())
            # result = Instruction.delete_by_id(valuesub)
            resp = redirect(url_for('instructions.start_page'))

        if 'addins' in request.form:
            resp = redirect(url_for('instructions.open_ins'))

    return resp


def open_ins():
    if 'back' in request.form:
        return redirect(url_for('instructions.start_page'))

    arg_id = request.args.get('id')
    if arg_id is not None:
        ins = Instruction.get_by_id(arg_id)
        form = InstructionForm(request.form or None, obj=ins)
        text = ins.text
        titleform = 'Изменить инструкцию'
    else:
        form = InstructionForm(request.form or None)
        titleform = 'Добавить инструкцию'
        text = ''

    if request.method == 'POST' and form.validate():
        text = request.form['text']
        d = datetime.today()
        if arg_id is not None:
            (Instruction
             .update(text=text,
                     name=form.name.data,
                     isactive=form.isactive.data,
                     changedate=d,
                     user=session.user.id)
             .where(Instruction.id == arg_id)
             .execute())
        else:
            ins = Instruction(text=text,
                              name=form.name.data,
                              isactive=form.isactive.data,
                              createdate=d,
                              changedate=d,
                              user=session.user.id)
            ins.save()
        return redirect(url_for('instructions.start_page'))

    return render_template('faqform.html', title=titleform,
                           form=form, text=text)
