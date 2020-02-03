from datetime import datetime
from app.models.instructions import Instruction


def test_res200(client):
    res = client.get('/instructions', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/instructions',
                      data={'addins': ''},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/instructions/openins', follow_redirects=True)
    assert res.status_code == 200


def test_dbtable(client, temp):
    res = client.post('/instructions/openins',
                      data={'name': 'new',
                            'user': 1,
                            'isactive': True,
                            'text': 'new',
                            'changedate': datetime.today(),
                            'createdate': datetime.today()},
                      follow_redirects=True)
    assert res.status_code == 200

    item = Instruction.get_by_id(1)
    assert item is not None

    res = client.post('/instructions',
                      data={'changeins': '1'},
                      follow_redirects=True)
    assert res.status_code == 200

    res = client.get('/instructions/openins?id=1', follow_redirects=True)
    assert res.status_code == 200

    res = client.post('/instructions',
                      data={'delins': '1'},
                      follow_redirects=True)
    assert res.status_code == 200
