
from ina219 import INA219
import logging
from machine import Pin, I2C
from utime import time
import _thread


class INA219Service:
    """Service wrapper for reading data from an INA219 module

"""


    def __init__(self, settings, log_level=logging.INFO):
        self.name = settings['name']
        logging.basicConfig(level=log_level)
        self.__log = logging.getLogger('INA219Service')
        self._i2c = I2C(-1, Pin(22), Pin(21))
        self._ina219 = INA219(settings['shunt_ohms'],
                              self._i2c,
                              log_level=logging.INFO,
                              address=(0x40 | settings['address']))
        self._ina219.configure()

        self.cache_60sec = []


    def start(self):
        """Start a thread to monitor the INA219 sensor"""
        _thread.start_new_thread(self.run, ())

    def run(self):
        """The function to run as a thread to monitor the INA219 sensor"""

        self.__log.info("Starting monitor")
        while True:
            latest_voltage = []
            latest_current = []
            latest_power = []
            nexttime = time() + 1

            while time() < nexttime:

                latest_voltage.append(self._ina219.voltage())
                current = self._ina219.current()
                latest_current.append(current)

                power = self._ina219.power()
                if current < 0.0:
                    power = power * -1  # convert to negative
                latest_power.append(power)

            # this is not quite how I want to do this!
            # pass the values in, but for now I want to be able
            # to see latest_*
            self.cache_append(nexttime,
                              latest_voltage,
                              latest_current,
                              latest_power)

    def cache_append(self, timestamp, voltage, current, power):
        """Write latest results to the 60sec cache and rotate it if necessary"""

        if len(self.cache_60sec) >= 60:
            self.__log.debug("Rotating cache")
            self.cache_60sec = self.cache_60sec[1:]

        self.__log.debug("Updating cache")
        self.cache_60sec.append((
            timestamp,
            sum(voltage) / len(voltage),
            sum(current) / len(current),
            sum(power) / len(power)
            ))

    def voltage(self):
        """Get latest voltage value"""
        return self.cache_60sec[-1][1]

    def current(self):
        """Get latest current value"""
        return self.cache_60sec[-1][2]

    def power(self):
        """Get latest power value"""
        return self.cache_60sec[-1][3]
