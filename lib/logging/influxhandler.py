import etc
from httpclient import http_post
import logging

settings = etc.get_config('influxdb.json')

class InfluxDBHandler(logging.Handler):

    timeoffset = 946684800

    severity_lookup = {
        50: 'crit',
        40: 'err',
        30: 'warning',
        20: 'info',
        10: 'debug'
        }

    severity_code_lookup = {
        50: 2,
        40: 3,
        30: 4,
        20: 6,
        10: 7
        }


    def __init__(self):
        self._url = 'http://{}:{}/write?db=syslog'.format(settings['connections'][0]['host'], settings['connections'][0]['port'])
        self._recordfmt = 'syslog,appname={appname},facility=console,host={host},hostname={hostname},severity={severity} facility=14i,message="{message}",severity_code={severity_code}i,procid="1",timestamp={timestamp}000000000i,version=1i'

    def _msg(self, record):
        return self._recordfmt.format(
            appname=record.name,
            host=settings['host'],
            hostname=settings['host'],
            severity=InfluxDBHandler.severity_lookup[record.levelno],
            message=record.msg,
            severity_code=InfluxDBHandler.severity_code_lookup[record.levelno],
            timestamp=(int(record.created) + InfluxDBHandler.timeoffset))

    def emit(self, record):

        http_post(self._url,
                  [self._msg(record)])

# syslog,appname=myapp,facility=console,host=myhost,hostname=myhost,severity=warning facility_code=14i,message="warning message here",severity_code=4i,procid="12345",timestamp=1534418426076077000i,version=1i

# syslog,appname=mysecondapp,facility=console,host=myhost,hostname=myhost,severity=crit facility_code=14i,message="critical message here",severity_code=2i,procid="12346",timestamp=1534418426076078000i,version=1i
