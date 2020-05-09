import etc
from httpclient import http_post
import json
import _thread
import time

settings = etc.get_config('influxdb.json')

def create_dbs():
    for c in settings['connections']:
        http_post('http://%s:%s/query' % (c['host'], c['port']),
                  ['q=CREATE DATABASE %s' % c['db']])


def send_to_influxdb(ina):
    for c in settings['connections']:
        http_post('http://%s:%s/write?db=%s' % (c['host'], c['port'], c['db']), [
                "bus_voltage,host=%s value=%.3f" % (settings['host'], ina.voltage()),
                "current,host=%s value=%.3f" % (settings['host'], ina.current()),
                "power,host=%s value=%.3f" % (settings['host'], ina.power())
              ])


def start(ina):
    create_dbs()

    def t(ina):
        while True:
            send_to_influxdb(ina)
            time.sleep(1)
    _thread.start_new_thread(t, (ina,))
