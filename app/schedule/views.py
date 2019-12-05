from flask import render_template, request, flash, redirect, url_for, session
from datetime import date, timedelta, datetime, time
from app.models.calendar import Calendar
from app.admin.forms import CalendarForm

def get_week(prevw=None, nextw=None):
    #print(f'p {prevw}')
    #print(f'n {nextw}')
    
    if prevw is not None:
        td = timedelta(days=1)
        d = datetime.strptime(prevw, '%Y-%m-%d').date()-td
    elif nextw is not None:
        td = timedelta(days=1)  
        d = datetime.strptime(nextw, '%Y-%m-%d').date()+td
    else:    
        d = date.today()
    wd = date.isoweekday(d)
    
    days = []
    for i in range(0,7):
        if i < wd:
            razn = wd-i
            td = timedelta(days=razn)
            newd = d-td
        elif i > wd:
            razn = i-wd
            td = timedelta(days=razn)
            newd = d+td
        else:
            newd = d
            
        if i != 0:
            days.append(newd)
        else:
            td = timedelta(days=7)
            vsk = newd+td
    days.append(vsk)
    #print(days)
    return days

def get_schedule(prevw=None, nextw=None):
    days = get_week(prevw, nextw)
    
    sch = {}
    for d in days:
        sel = (Calendar
           .select()
           .where(Calendar.day == d)
           .order_by(Calendar.timestart))
        sch[d] = list(sel)
    #print(sch)
    return sch
    
def start_page():
    prevw = request.args.get('prev')
    nextw = request.args.get('next')
    days = get_week(prevw, nextw)
    sch = get_schedule(prevw, nextw)
    
    #-------#
    timet = datetime(1,1,1,8)
    print(timet)
    td = timedelta(minutes=5)
    times = []
    while timet <= datetime(1,1,1,16,30):
        times.append(timet.time())
        timet = timet+td
    #print(times)
    #-------#
    
    resp = render_template('calendar.html', title='Расписание конференц-зала', 
                           days=days, sch=sch, times=times)
    if request.method == 'POST':
        dictform = dict(request.form)
        if 'changesub' in request.form and 'evid' in request.form:
            valuesub = dictform['evid']
            resp = redirect(url_for('calendar.open_event', id=valuesub))
        
        if 'delsub' in request.form and 'evid' in request.form:
            valuesub = int(dictform['evid'])
            result = Calendar.delete_by_id(valuesub)
            resp = redirect(url_for('calendar.start_page'))
        
        if 'addevent' in request.form:
            resp = redirect(url_for('calendar.open_event'))
    
    return resp

def open_event():
    if 'back' in request.form:
        return redirect(url_for('calendar.start_page'))
    
    arg_id = request.args.get('id')
    if arg_id is not None:
        event = Calendar.get_by_id(arg_id)
        form = CalendarForm(request.form or None, obj=event)
        titleform = 'Изменить мероприятие'
    else:
        form = CalendarForm(request.form or None)
        titleform = 'Добавить мероприятие'
        
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            ev = event
            ev.day=form.day.data
            ev.timestart=form.timestart.data
            ev.timeend=form.timeend.data
            ev.event=form.event.data
            ev.resp=form.resp.data
            ev.comment=form.comment.data
        else:    
            ev = Calendar(day=form.day.data,
                          timestart=form.timestart.data,
                          timeend=form.timeend.data,
                          event=form.event.data,
                          resp=form.resp.data,
                          comment=form.comment.data)
        ev.save()
        return redirect(url_for('calendar.start_page'))
    
    return render_template('eventform.html', form=form, title = titleform)
