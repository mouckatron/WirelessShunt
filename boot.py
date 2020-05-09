import etc
import network
import ntptime
import time


# CONNECT TO NETWORK
wifi_settings = etc.get_config('wifi.json')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_settings['SSID'], wifi_settings['password'])

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
