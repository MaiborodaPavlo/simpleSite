import json


def test_content_type(json_handler):
    assert json_handler.content_type == 'application/json'


def test_json_data(json_handler):
    assert json_handler.data == json.loads(json.dumps(json_handler.data))


def test_json_data_format(json_handler):
    fields = ('status', 'message', 'data')
    for field in fields:
        assert field in json.loads(json_handler.data).keys()


def test_json_data_format_len(json_handler):
    assert len(json.loads(json_handler.data).keys()) == 3

