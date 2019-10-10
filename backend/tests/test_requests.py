import requests


def test_url_content():
    response = requests.get('http://localhost:8000/content')
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert response.json()['message'] == ''
    assert isinstance(response.json()['data'], list)


def test_wrong_urls():
    response = requests.get('http://localhost:8000/spam')
    assert response.status_code == 404


def test_wrong_method():
    response = requests.put('http://localhost:8000/content', files=dict(foo='bar'))
    assert response.status_code == 501


def test_post():
    response = requests.post('http://localhost:8000/content', data={"service_id": 1, "servtype": "srv_vps", "subtype": "SSD-VPS-2-0317", "user_id": 664082,
       "referrer_user_id": 664082, "state": "D", "creation_date": "2018-02-12", "creation_time": "08:31:24",
       "creation_request_sent_date": "0000-00-00 00:00:00", "notified_about_expiration": -3}, files=dict(foo='bar'))

    assert response.status_code == 200


def test_put():
    response = requests.put('http://localhost:8000/content/1', data={"service_id": 1, "servtype": "srv_vps", "subtype": "SSD-VPS-2-0317", "user_id": 664082,
       "referrer_user_id": 664082, "state": "D", "creation_date": "2018-02-12", "creation_time": "08:31:24",
       "creation_request_sent_date": "0000-00-00 00:00:00", "notified_about_expiration": 10}, files=dict(foo='bar'))

    assert response.status_code == 200


def test_delete():
    response = requests.delete('http://localhost:8000/content/1')

    assert response.status_code == 200


def test_upload():
    files = {'file': open('tests/table_task1.csv', 'rb')}
    response = requests.post('http://localhost:8000/content/upload',
                             files=files)

    assert response.status_code == 200

