import json
import re
import socket
import _thread


class Webserver():

    request_re = re.compile('(GET|HEAD|POST)\s+(\S+)\s+(HTTP)/([0-9.]+)')

    def __init__(self, routes={}):
        self.routes = routes

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            request = conn.recv(1024)

            print(request)

            parsed_request = self.parse_request(request)
            if parsed_request is not None:
                route = self.find_route(parsed_request['path'])
            else:
                route = None

            if parsed_request is None:
                conn.send('HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n')

            elif route is None:
                conn.send('HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n')

            else:
                conn.send('HTTP/1.1 200 OK\r\nConnection: close\r\n')
                conn.send('\r\n'.join(route.__class__.headers))
                conn.send('\r\n\r\n')
                conn.send(route.get_response())

            conn.close()

    def parse_request(self, request):
        try:
            first_line = request.decode('UTF-8').split("\r\n")[0].strip()
            print(first_line)
        except IndexError:
            return None

        parsed = Webserver.request_re.match(first_line)
        if parsed is None:
            return None

        return {
            'verb': parsed.group(1),
            'path': parsed.group(2),
            'version': parsed.group(4)
            }

    def find_route(self, path):

        try:
            self.routes[path]
        except KeyError:
            pass
        else:
            return self.routes[path]

        for r in self.routes:
            if path.find(r) > -1:
                return self.routes[r]

        return None


class Empty:

    headers = []

    def __init__(self, r=None):
        self.get_response = r


class JSONAPI:

    headers = [
        'Content-Type: text/json'
        ]

    def __init__(self, r=None):
        if r is not None:
            self.response = r

    def get_response(self):
        return json.dumps(self.response())

    def response(self):
        return {}


class HTMLPage:

    def get_response(self):
        return self.response()

    def response(self):
        return "<html><head><title>Hi!</title></head><body>Hi :) </body></html>"
