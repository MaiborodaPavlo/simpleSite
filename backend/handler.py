from http.server import BaseHTTPRequestHandler
import cgi

from router import Router
from response import BadResponse
from logger import logger, class_logger


class BadRequestException(Exception):

    def __init__(self, code=400, status='Bad request'):
        self.code = code
        self.status = status

        super().__init__()


@class_logger()
class HTTPRequestHandler(BaseHTTPRequestHandler):

    router = Router()

    def __init__(self, request, client_address, server):
        self._allow_methods = ('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')

        super().__init__(request, client_address, server)

    def __getattr__(self, name):
        if name in ('do_GET', 'do_DELETE'):
            return self.do_GET_DELETE
        elif name in ('do_POST', 'do_PUT'):
            return self.do_PUT_POST
        else:
            super().__getattr__(name)

    def do_OPTIONS(self):
        cors_method = self.headers.get('Access-Control-Request-Method')
        if cors_method in self._allow_methods:
            self.send_response(200, 'OK')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
            self.end_headers()
            self.flush_headers()
        else:
            logger.error(f'{cors_method} not allowed')
            self._respond(BadResponse(405, 'Method Not Allowed'))

    def do_GET_DELETE(self):
        response = self.router.routing(self.path, self.command)
        self._respond(response)

    def do_PUT_POST(self):

        try:
            form_data = self._get_form_data()
        except BadRequestException as ex:
            self._respond(BadResponse(ex.code, ex.status))

        response = self.router.routing(self.path, self.command, form_data)
        self._respond(response)

    def _get_form_data(self):

        try:
            content_type = self.headers['Content-Type']
        except KeyError as ex:
            logger.error(ex)
            raise BadRequestException()

        ctype, _ = cgi.parse_header(content_type)

        if ctype == 'multipart/form-data':
            if self.headers.get('Content-Length') != 0:
                fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                      environ={'REQUEST_METHOD': 'POST',
                                               'CONTENT_TYPE': content_type})

                form_data = {}

                for f in fs.list:
                    if f.filename:
                        form_data['filename'] = f.filename
                        form_data['data'] = f.file.read()
                    else:
                        form_data[f.name] = f.value
                return form_data
            else:
                logger.error('Content-Length must be not 0')
                raise BadRequestException()
        else:
            logger.error(f'{ctype} not supported')
            raise BadRequestException(501, 'Not Implemented')

    def _handle_http(self, handler):
        status_code = handler.status_code
        if status_code is 200:
            self.send_response(status_code, handler.status_message)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', handler.content_type)
            self.end_headers()
        else:
            self.send_error(status_code, message=handler.status_message)
            return

        return bytes(handler.data, 'UTF-8')

    def _respond(self, handler):
        response = self._handle_http(handler)
        if response is not None:
            self.wfile.write(response)

