from datetime import datetime
from app.models.news import News


def test_res200(client):
    res = client.get('/', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/',
                      data={'addnews': ''},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/opennews', follow_redirects=True)
    assert res.status_code == 200


def test_dbtable(client, temp):
    res = client.post('/opennews',
                      data={'name': 'new',
                            'user': 1,
                            'typenews': 1,
                            'isactive': True,
                            'text': 'new',
                            'changedate': datetime.today(),
                            'createdate': datetime.today()},
                      follow_redirects=True)
    assert res.status_code == 200

    item = News.get_by_id(1)
    assert item is not None

    res = client.post('/',
                      data={'changenews': '1'},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/opennews?id=1', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/',
                      data={'delnews': '1'},
                      follow_redirects=True)
    assert res.status_code == 200
