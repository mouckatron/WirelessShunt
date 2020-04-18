import setup

from machine import Pin, I2C
from logging import INFO
from ina219 import INA219
import webserver
import influxdb
import time
import _thread

SHUNT_OHMS = 0.05

i2c = I2C(-1, Pin(22), Pin(21))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()


# webserver.start(ina)

influxdb.create_dbs()
influxdb.start(ina)


def console_out(ina):
    while True:
        print("%.3fV %.3fmA %.3fmW" %
              (ina.voltage(), ina.current(), ina.power()))
        time.sleep(1)


_thread.start_new_thread(console_out, (ina,))
