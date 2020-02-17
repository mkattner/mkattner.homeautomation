from main.ota_updater import OTAUpdater


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


#ap_if = network.WLAN(network.AP_IF)
#ap_if.active(False)

#station = network.WLAN(network.STA_IF)
#station.active(True)
#station.connect(wifi_ssid, wifi_password)
#while station.isconnected() == False:
#  pass

print('Wifi connection successful')
print('IP settings:' )
print(station.ifconfig())



def download_and_install_update_if_available():
  ota_updater = OTAUpdater('https://github.com/mkattner/mkattner.homeautomation/')
  ota_updater.download_and_install_update_if_available(wifi_ssid, wifi_password)

def start():
  import main.start
  # your custom code goes here. Something like this: ...
  # from main.x import YourProject
  # project = YourProject()
  # ...

def boot():
  download_and_install_update_if_available()
  start()


boot()