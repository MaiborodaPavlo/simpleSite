import json
import pytest

from response import JSONResponse
from controllers import ContentController


class MockServicesModel:
    @staticmethod
    def __init__():
        pass

    @staticmethod
    def get_all():
        return [{'service_id': 1, 'servtype': 'srv_license_isp', 'subtype': 'lite6', 'user_id': 45532, 'referrer_user_id': 26532, 'state': 'O', 'creation_date': '2017-08-18', 'creation_time': '16:04:56', 'creation_request_sent_date': None, 'notified_about_expiration': 0}, {'service_id': 22624301, 'servtype': 'srv_hosting_ispmgr', 'subtype': 'Host-Lite-0910', 'user_id': 46544, 'referrer_user_id': 26532, 'state': 'D', 'creation_date': '2016-09-23', 'creation_time': '22:50:50', 'creation_request_sent_date': '2010-02-27 16:52:58', 'notified_about_expiration': 5}, {'service_id': 22712397, 'servtype': 'srv_vps', 'subtype': 'WIN-3', 'user_id': 345532, 'referrer_user_id': 26532, 'state': 'A', 'creation_date': '2016-09-29', 'creation_time': '9:53:40', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': 0}, {'service_id': 23200637, 'servtype': 'srv_parallels_wpb', 'subtype': 'WPB-Standart', 'user_id': 664082, 'referrer_user_id': 26532, 'state': 'A', 'creation_date': '2016-10-26', 'creation_time': '11:03:20', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': 127}, {'service_id': 27088203, 'servtype': 'srv_vps', 'subtype': 'SSD-VPS-1-0317', 'user_id': 26532, 'referrer_user_id': 26532, 'state': 'S', 'creation_date': '2017-03-06', 'creation_time': '13:06:35', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': 3}, {'service_id': 29414795, 'servtype': 'srv_vps', 'subtype': 'XEN-2-1216', 'user_id': 26112, 'referrer_user_id': 26532, 'state': 'D', 'creation_date': '2017-06-06', 'creation_time': '11:20:34', 'creation_request_sent_date': '2010-03-02 16:59:55', 'notified_about_expiration': 3}, {'service_id': 30951405, 'servtype': 'srv_license_isp', 'subtype': 'lite5', 'user_id': 45532, 'referrer_user_id': 26532, 'state': 'O', 'creation_date': '2017-08-18', 'creation_time': '16:04:41', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': 0}, {'service_id': 32866369, 'servtype': 'srv_google_apps', 'subtype': 'trial', 'user_id': 382636, 'referrer_user_id': 393221, 'state': 'D', 'creation_date': '2017-11-03', 'creation_time': '9:02:42', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': 1}, {'service_id': 34490653, 'servtype': 'srv_websitebuilder', 'subtype': 'start', 'user_id': 208949, 'referrer_user_id': 26532, 'state': 'A', 'creation_date': '2018-01-11', 'creation_time': '21:51:38', 'creation_request_sent_date': '2010-03-12 11:25:45', 'notified_about_expiration': 0}, {'service_id': 35109397, 'servtype': 'srv_vps', 'subtype': 'SSD-VPS-2-0317', 'user_id': 664082, 'referrer_user_id': 664082, 'state': 'D', 'creation_date': '2018-02-12', 'creation_time': '8:31:24', 'creation_request_sent_date': '0000-00-00 00:00:00', 'notified_about_expiration': -3}, {'service_id': 35109399, 'servtype': 'srv_license_isp', 'subtype': 'lite5', 'user_id': 664082, 'referrer_user_id': 664082, 'state': 'S', 'creation_date': '2018-02-12', 'creation_time': '8:29:22', 'creation_request_sent_date': '2012-07-12 12:40:15', 'notified_about_expiration': 55}]

    @staticmethod
    def delete_row(id_):
        return 1 if id_ else 0

    @staticmethod
    def add_row(services_row):
        if services_row.service_id == 1:
            return 0
        else:
            return 1


@pytest.fixture
def mocked_controller(monkeypatch):
    def mock_model_init(self):
        self._model = MockServicesModel()

    monkeypatch.setattr(ContentController, '__init__', mock_model_init)

    return ContentController()


def test_get_action(data, mocked_controller):

    result = mocked_controller.get_action()

    assert isinstance(result, JSONResponse)
    assert result.data is not None
    assert json.loads(result.data)['data'] == data


def test_delete_action(mocked_controller):

    id_ = 0

    result = mocked_controller.delete_action(id_)

    assert isinstance(result, JSONResponse)
    assert result.json_status == 'error'

    id_ = 1
    result = mocked_controller.delete_action(id_)

    assert isinstance(result, JSONResponse)
    assert result.json_status == 'success'
