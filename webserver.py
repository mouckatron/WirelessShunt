import json
import logging
import re
import socket
import _thread
from time import sleep


class Webserver():

    request_re = re.compile('(GET|HEAD|POST)\s+(\S+)\s+(HTTP)/([0-9.]+)')

    def __init__(self, routes={}):
        self.routes = routes
        self._log = logging.getLogger('WEB')
        self.__bound = False

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not self.__bound:
            # somtimes during a soft reset, we cannot rebind the socket, keep trying
            try:
                s.bind(('', 80))
                self.__bound = True
            except OSError as e:
                self._log.error(str(e))
                sleep(1)

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
            self._log.error("Could not find route {}".format(path))
        else:
            return self.routes[path]

        # What is this code doing? We probably would not get here.
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

    headers = [
        'Content-Type: text/html'
        ]

    def __init__(self, template_filename, template_vars=None):
        self.template_filename = template_filename
        if template_vars is not None:
            self.get_vars = template_vars

    def get_response(self):
        return self.response()

    def response(self):
        try:
            with open(self.template_filename, 'r') as f:
                content = f.read()
        except Exception as e:
            print(e)
        else:
            try:
                return content.format(**self.get_vars())
            except KeyError as e:
                print(e)
                return str(e)

    def get_vars(self):
        return {}
