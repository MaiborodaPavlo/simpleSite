from models import ServicesRow, ServicesModel


def test_services_row_repr1():
    data = {'service_id': '1', 'servtype': 'srv_license_isp', 'subtype': 'lite6',
            'user_id': '45532', 'referrer_user_id': '26532', 'state': 'O',
            'creation_date': '2017-08-18', 'creation_time': '16:04:56',
            'creation_request_sent_date': 'null', 'notified_about_expiration': '0'}

    s_row = ServicesRow(data)

    assert f'{s_row}' == "1, 'srv_license_isp', 'lite6', 45532, 26532, 'O', " \
                         "'2017-08-18', '16:04:56', default(creation_request_sent_date), 0"


def test_services_row_repr2():
    data = {'service_id': '1', 'servtype': 'srv_license_isp', 'subtype': 'lite6',
            'user_id': '45532', 'referrer_user_id': '26532', 'state': 'O',
            'creation_date': '2017-08-18', 'creation_time': '16:04:56',
            'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': '0'}

    s_row = ServicesRow(data)

    assert f'{s_row}' == "1, 'srv_license_isp', 'lite6', 45532, 26532, 'O', " \
                         "'2017-08-18', '16:04:56', default(creation_request_sent_date), 0"


def test_services_row_is_valid():
    data = {'servtype': 'srv_license_isp', 'subtype': 'lite6',
            'user_id': '45532', 'referrer_user_id': '26532', 'state': 'O',
            'creation_date': '2017-08-18', 'creation_time': '16:04:56',
            'creation_request_sent_date': 'null', 'notified_about_expiration': '0'}

    s_row = ServicesRow(data)

    assert not s_row.is_valid()

