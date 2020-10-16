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


class InfluxDBWriter:
    """Send shunt data to InfluxDB"""

    def __init__(self, settings, sensor_service):
        self.settings = settings
        self.sensor_service = sensor_service

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            v, c, p = None, None, None
            try:
                v = self.sensor_service.voltage()
                c = self.sensor_service.current()
                p = self.sensor_service.power()

            except:
                # in case we get an exception upstream
                time.sleep(1)
                continue

            msg = ["bus_voltage,host=%s,sensor=%s value=%.3f" %
                   (settings['host'], self.sensor_service.name, v),
                   "current,host=%s,sensor=%s value=%.3f" %
                   (settings['host'], self.sensor_service.name, c),
                   "power,host=%s,sensor=%s value=%.3f" %
                   (settings['host'], self.sensor_service.name, p)]
            for conn in settings['connections']:
                http_post('http://%s:%s/write?db=%s' % (conn['host'],
                                                        conn['port'],
                                                        conn['db']),
                          msg)
            time.sleep(1)
