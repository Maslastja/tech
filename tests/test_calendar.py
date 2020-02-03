from datetime import date, time
from app.models.calendar import Calendar


def test_res200(client, temp):
    res = client.get('/calendar', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/calendar',
                      data={'addevent': ''},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/calendar/openevent', follow_redirects=True)
    assert res.status_code == 200


def test_dbtable(client, temp):
    res = client.post('/calendar/openevent',
                      data={'day': date.today(),
                            'timestart': time(11, 0),
                            'timeend': time(11, 30),
                            'event': 'new',
                            'resp': 'new',
                            'comment': 'new'},
                      follow_redirects=True)
    assert res.status_code == 200

    item = Calendar.get_by_id(1)
    assert item is not None

    res = client.post('/calendar',
                      data={'changesub': '',
                            'evid': '1'},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/calendar/openevent?id=1', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/calendar',
                      data={'delsub': '',
                            'evid': '1'},
                      follow_redirects=True)
    assert res.status_code == 200
