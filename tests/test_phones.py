import requests
from app.models.phones import Phones


def test_res200(client):
    res = client.get('/phones', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/phones',
                      data={'addsub': ''},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/openphone', follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/phoneslist', follow_redirects=True)
    assert res.status_code == 200


def test_dbtable(client, temp):
    res = client.post('/openphone',
                      data={'fil': 'irk',
                            'otd': 'irk.nonmed.54',
                            'typeotd': 'nonmed',
                            'nameabon': 'new',
                            'numberin': '123',
                            'numberout': '123',
                            'email': 'mail@mail.ru',
                            'isgeneral': True,
                            'isactive': True,
                            'comment': 'new'},
                      follow_redirects=True)
    assert res.status_code == 200

    item = Phones.get_by_id(1)
    assert item is not None

    res = client.post('/phones',
                      data={'changesub': '1'},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/openphone?id=1', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/phones',
                      data={'delsub': '1'},
                      follow_redirects=True)
    assert res.status_code == 200

    temp.close()
    with client.session_transaction() as session:
        requests.post(f'http://auth.iood.ru/sess/{session.sid}/close')
