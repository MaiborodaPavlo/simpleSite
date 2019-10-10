from http.server import HTTPServer

from handler import HTTPRequestHandler
from logger import logger, class_logger
import config


@class_logger()
class Server:

    def __init__(self, host=None, port=None, handler=HTTPRequestHandler):
        self.host = host or config.get_setting(config.PATH, 'Connection', 'host')
        self.port = port or int(config.get_setting(config.PATH, 'Connection', 'port'))
        self.handler = handler
        self.httpd = HTTPServer((self.host, self.port), self.handler)

    def run(self):
        logger.info(f'Server Starts - {self.host}:{self.port}')
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.server_close()
        logger.info(f'Server Stops - {self.host}:{self.port}')

    def add_route(self, *route):
        self.handler.router.route(*route)
