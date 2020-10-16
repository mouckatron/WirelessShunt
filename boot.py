import etc
import network
import ntptime
import time


# CONNECT TO NETWORK
wifi_settings = etc.get_config('wifi.json')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while not wlan.isconnected():
    available_networks = [x[0] for x in wlan.scan()]
    for wifi in wifi_settings:
        if wifi['SSID'] in available_networks:
            wlan.connect(wifi['SSID'], wifi['password'])
            time.sleep(1)
            if not wlan.isconnected():
                wlan.disconnect()

    if not wlan.isconnected():
        print("Could not connect to a known network")
        for x in available_networks:
            print(x[0])
        time.sleep(5)

# SET TIME
try:
    ntptime.settime()
except OSError:
    time.sleep(1)
    try:
        ntptime.settime()
    except OSError:
        pass
