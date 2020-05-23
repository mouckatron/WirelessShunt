import setup

import etc
from machine import reset
from ina219service import INA219Service
from logging import DEBUG
import webserver
import influxdb
import systemutils
import svgchart

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
web_dashboard = webserver.HTMLPage(
    'html/dashboard.html',
    lambda: {
        'df': systemutils.df(),
        'free': systemutils.free(),
        'voltage_graph': str(svgchart.SVGChart([x[1] for x in inas.cache_60sec], size=(500,200), show_zero=True)),
        'current_graph': str(svgchart.SVGChart([x[2]/1000.0 for x in inas.cache_60sec], size=(500,200))),
        'power_graph': str(svgchart.SVGChart([x[3]/1000.0 for x in inas.cache_60sec], size=(500,200)))
    })

web = webserver.Webserver(routes={
    '/api': web_api,
    '/reset': web_reset,
    '/dashboard': web_dashboard
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
