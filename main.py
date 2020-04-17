import setup

from machine import Pin, I2C
from logging import INFO
from ina219 import INA219
import webserver
from influxdb import send_to_influxdb
import time

SHUNT_OHMS = 0.05

i2c = I2C(-1, Pin(22), Pin(21))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()


# webserver.start(ina)

while True:
    print("Bus Voltage: %.3f V" % ina.voltage())
    print("Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())

    send_to_influxdb(ina)

    time.sleep(1)
