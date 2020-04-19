import setup

from machine import Pin, I2C, reset
from logging import INFO
from ina219 import INA219
import webserver
import influxdb

SHUNT_OHMS = 0.001

i2c = I2C(-1, Pin(22), Pin(21))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()


# WEBSERVER
web_api = webserver.JSONAPI(lambda: {
    'bus_voltage': '%.3f' % ina.voltage(),
    'current': '%.3f' % ina.current(),
    'power': '%.3f' % ina.power()
    })
web_reset = webserver.Empty(lambda: reset())

web = webserver.Webserver(routes={
    '/api': web_api,
    '/reset': web_reset
    })
web.start()


# INFLUXDB
influxdb.create_dbs()
influxdb.start(ina)


# def console_out(ina):
#     while True:
#         print("%.3fV %.3fmA %.3fmW" %
#               (ina.voltage(), ina.current(), ina.power()))
#         time.sleep(1)


# _thread.start_new_thread(console_out, (ina,))
