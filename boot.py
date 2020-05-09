import json
import network
import ntptime
import time


# CONNECT TO NETWORK
settings = None
with open('wifi.json', 'r') as f:
    settings = json.loads(f.read())

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(settings['SSID'], settings['password'])

while not wlan.isconnected():
    pass

# SET TIME
try:
    ntptime.settime()
except OSError:
    time.sleep(1)
    try:
        ntptime.settime()
    except OSError:
        pass
