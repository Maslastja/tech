import json
import peewee as pw
from flask import render_template, request, redirect, url_for
from datetime import date, timedelta, datetime
from app.models.calendar import Calendar
from app.admin.forms import CalendarForm


def get_week(prevw=None, nextw=None):
    # print(f'p {prevw}')
    # print(f'n {nextw}')

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
    for i in range(0, 7):
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
    # print(days)
    return days


def times():
    timet = datetime(1, 1, 1, 8)
    td = timedelta(minutes=5)
    times = []
    # while timet <= datetime(1, 1, 1, 16, 30):
    while timet <= datetime(1, 1, 1, 16, 55):
        times.append(timet.time())
        timet = timet+td

    return times


def get_schedule(prevw=None, nextw=None):
    days = get_week(prevw, nextw)
    sch = {}
    timeslist = times()
    qs = (Calendar
          .select(Calendar.day,
                  pw.fn.collect(Calendar.id,
                                Calendar.timestart,
                                Calendar.timeend,
                                Calendar.event,
                                Calendar.comment,
                                Calendar.resp
                                ).alias('events'))
          .where(Calendar.day.between(days[0], days[6]))
          .group_by(Calendar.day)
          .order_by(Calendar.day, Calendar.timestart)
          .dicts())

    for d in days:
        sch[d] = {}

    for q in qs:
        events = json.loads(q['events'])
        dict_for_order = {}
        for ev in events:
            ev['timestart'] = (datetime
                               .strptime(ev['timestart'], '%H:%M:%S')
                               .time())
            ev['timeend'] = (datetime
                             .strptime(ev['timeend'], '%H:%M:%S')
                             .time())
            ev['evtime'] = ([t for t in timeslist if (t >= ev['timestart'] and
                                                      t < ev['timeend'])])
            dict_for_order[ev['timestart']] = ev

        list_keys = list(dict_for_order.keys())
        list_keys.sort()
        events = []
        for i in list_keys:
            events.append(dict_for_order[i])
        sch[q['day']] = events
    return sch


def get_endevents(sch):
    endev = {}
    for d in sch:
        for ev in sch[d]:
            endev[d] = ev['evtime'][len(ev['evtime'])-1]

    return endev


def start_page():
    prevw = request.args.get('prev')
    nextw = request.args.get('next')
    days = get_week(prevw, nextw)
    sch = get_schedule(prevw, nextw)
    endev = get_endevents(sch)
    if request.method == 'POST':
        if 'changesub' in request.form and 'evid' in request.form:
            valuesub = request.form['evid']
            url = url_for('calendar.open_event', id=valuesub)

        if 'delsub' in request.form and 'evid' in request.form:
            valuesub = int(request.form['evid'])
            Calendar.delete_by_id(valuesub)
            url = url_for('calendar.start_page')

        if 'addevent' in request.form:
            url = url_for('calendar.open_event')
        return redirect(url)

    return render_template('calendar.html', title='Расписание конференц-зала',
                           days=days, sch=sch, times=times(), endev=endev)


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
            ev.day = form.day.data
            ev.timestart = form.timestart.data
            ev.timeend = form.timeend.data
            ev.event = form.event.data
            ev.resp = form.resp.data
            ev.comment = form.comment.data
        else:
            ev = Calendar(day=form.day.data,
                          timestart=form.timestart.data,
                          timeend=form.timeend.data,
                          event=form.event.data,
                          resp=form.resp.data,
                          comment=form.comment.data)
        ev.save()
        return redirect(url_for('calendar.start_page'))

    return render_template('eventform.html', form=form, title=titleform)
