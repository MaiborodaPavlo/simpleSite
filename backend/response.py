import json


class Response:

    def __init__(self, status_code=200, status_message='OK'):
        self.status_code = status_code
        self.status_message = status_message
        self.content_type = ''


class JSONResponse(Response):

    def __init__(self, data=None, json_status='success', json_mes=''):
        super().__init__()

        self._data = data
        self.content_type = 'application/json'
        self.json_status = json_status
        self.json_mes = json_mes

    @property
    def data(self):
        return json.dumps({'status': self.json_status, 'message': self.json_mes, 'data': self._data})


class BadResponse(Response):

    def __init__(self, status_code=404, status_message='Not Found'):
        super().__init__(status_code, status_message)

