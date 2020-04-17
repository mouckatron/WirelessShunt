import socket
import json

# class Webserver(_thread.Thread):


def start(ina):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)

        print(request)

        conn.send('HTTP/1.1 200 OK\n')

        if request.find('/api') == 6:
            response = api(conn, ina)

        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


def api(conn, ina):
    conn.send('Content-Type: text/json\n')

    output = {
        'bus_voltage': '%.3f' % ina.voltage(),
        'current': '%.3f' % ina.current(),
        'power': '%.3f' % ina.power()
        }
    return json.dumps(output)
