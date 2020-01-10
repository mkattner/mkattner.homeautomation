# https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy
# https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
import globals
gc.collect()

print();


print("START device " + globals.device_name)

#WIFI
wifi_ssid = 'stygs.com'
wifi_password = 'SauerMachtLustig'
mqtt_server = '192.168.1.50'

#MQTT
mqtt_port = 1883
mqtt_user = "mqtt"
mqtt_password = "mqtt"
mqtt_client_id = ubinascii.hexlify(machine.unique_id())

#HOME ASSISTANT
ha_prefix = "homeassistant/"


ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifi_ssid, wifi_password)
while station.isconnected() == False:
  pass

print('Wifi connection successful')
print('IP settings:' )
print(station.ifconfig())
