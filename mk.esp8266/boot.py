import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

print("START")

ssid = 'stygs.com'
password = 'SauerMachtLustig'
mqtt_server = '192.168.1.50'
mqtt_port = 1883
mqtt_user = "mqtt"
mqtt_password = "mqtt"

#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'

client_id = ubinascii.hexlify(machine.unique_id())



ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())