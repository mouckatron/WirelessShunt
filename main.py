import setup

import etc
from machine import reset
from ina219service import INA219Service
from logging import DEBUG
import webserver
import influxdb

# INA219
ina219_settings = etc.get_config('ina219.json')
inas = INA219Service(ina219_settings['shunt1'])
inas.start()

# WEBSERVER
web_api = webserver.JSONAPI(lambda: {
    'bus_voltage': '%.3f' % inas.voltage(),
    'current': '%.3f' % inas.current(),
    'power': '%.3f' % inas.power()
    })
web_reset = webserver.Empty(lambda: reset())

web = webserver.Webserver(routes={
    '/api': web_api,
    '/reset': web_reset
    })
web.start()


# influxdb
influxdb.create_dbs()
influxdb.start(inas)


# def console_out(ina):
#     while True:
#         print("%.3fV %.3fmA %.3fmW" %
#               (ina.voltage(), ina.current(), ina.power()))
#         time.sleep(1)


# _thread.start_new_thread(console_out, (ina,))
