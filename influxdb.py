import socket
import json

settings = None
with open('influxdb.json') as f:
    settings = json.loads(f.read())


def send_to_influxdb(ina):

    http_post('http://%s:%s/write?db=%s' % (settings['host'], settings['port'], settings['db']),
              [
                "bus_voltage,host=solarshunt value=%.3f" % ina.voltage(),
                "current,host=solarshunt value=%.3f" % ina.current(),
                "power,host=solarshunt value=%.3f" % ina.power()
              ])


def http_post(url, data_lines):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 8086)[0][-1]
    s = socket.socket()
    s.connect(addr)

    head = [
        'POST /%s HTTP/1.1' % path,
        'Host: %s:8086' % host,
        'User-Agent: MicroPython',
        'Accept: *',
        'Content-Length: %s' % len("\n".join(data_lines)),
        'Content-Type: application/x-www-form-urlencoded',
        '', ''
        ]

    s.send(bytes("\r\n".join(head) + "\n".join(data_lines), 'utf8'))

    data = s.recv(1024)
    if data:
        print(str(data, 'utf8'))

    s.close()
