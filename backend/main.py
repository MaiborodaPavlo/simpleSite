import argparse

from server import Server

parser = argparse.ArgumentParser(description='Конфигурация работы сервера')
parser.add_argument('--host', help='Укажите адрес хоста')
parser.add_argument('--port', help='Укажите порт хоста')

host = parser.parse_args().host
port = int(parser.parse_args().port) if parser.parse_args().port else None

server = Server(host, port)

server.add_route('/content/upload', 'POST', 'ContentController', 'upload_action')
server.add_route('/content', 'GET', 'ContentController', 'get_action')
server.add_route('/content', 'POST', 'ContentController', 'post_action')
server.add_route(r'/content/(\d*)$', 'PUT', 'ContentController', 'put_action')
server.add_route(r'/content/(\d*)$', 'DELETE', 'ContentController', 'delete_action')

try:
    server.run()

except KeyboardInterrupt:
    server.stop()


