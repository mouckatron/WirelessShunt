import setup

import etc
import machine
from ina219service import INA219Service
import logging
import logging.influxhandler
import webserver
import influxdb
import systemutils
import svgchart

# Logging
logging.getLogger().setLevel(logging.INFO)

# Initial WEB
web_routes = {}
web_reset = webserver.Empty(lambda: machine.reset())

# INA219
ina219_settings = etc.get_config('ina219.json')
inas = {}
for sensor in ina219_settings:
    inas[sensor] = INA219Service(ina219_settings[sensor])
    inas[sensor].start()
    web_routes['api/{}'.format(sensor)] = webserver.JSONAPI(lambda sensor: {
        'bus_voltage': '%.3f' % inas[sensor].voltage(),
        'current': '%.3f' % inas[sensor].current(),
        'power': '%.3f' % inas[sensor].power()
        })
    web_dashboard = webserver.HTMLPage(
        'html/dashboard.html',
        lambda sensor: {
            'df': systemutils.df(),
            'free': systemutils.free(),
            'voltage_graph': str(svgchart.SVGChart([x[1] for x in inas[sensor].cache_60sec], size=(500,200), show_zero=True)),
            'current_graph': str(svgchart.SVGChart([x[2]/1000.0 for x in inas[sensor].cache_60sec], size=(500,200))),
            'power_graph': str(svgchart.SVGChart([x[3]/1000.0 for x in inas[sensor].cache_60sec], size=(500,200)))
            })

# WEBSERVER
web = webserver.Webserver(web_routes)
web.start()


# INFLUXDB
influxdb.create_dbs()
dbs = {}
for sensor in inas:
    dbs[sensor] = influxdb.InfluxDBWriter(influxdb.settings, inas[sensor])
    dbs[sensor].start()
