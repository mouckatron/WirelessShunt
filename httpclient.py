import socket


def http_post(url, data_lines, return_data=False):
    _, _, host, path = url.split('/', 3)
    host, port = host.split(':')
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)

    head = [
        'POST /%s HTTP/1.1' % path,
        'Host: %s:%s' % (host, port),
        'User-Agent: MicroPython',
        'Accept: *',
        'Content-Length: %s' % len("\n".join(data_lines)),
        'Content-Type: application/x-www-form-urlencoded',
        '', ''
        ]

    s.send(bytes("\r\n".join(head) + "\n".join(data_lines), 'utf8'))

    if return_data:
        output = ""
        data = s.recv(2048)
        if data:
            output = str(data, 'utf8')

    s.close()

    if return_data:
        return output
