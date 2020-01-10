import time, machine

def restart_and_reconnect():
  print('Something has failed: reboot')
  time.sleep(10)
  machine.reset()

device_name = 'WZ1'

SWITCH_0_load = False
DS1820B_0_load = False
DHT11_0_load = False

BME_280_0_load            = True
BME280_0_CONFIG_TOPIC_T   = ('homeassistant/sensor/'+device_name+'_BME280_0_T/config').encode()
BME280_0_CONFIG_TOPIC_H   = ('homeassistant/sensor/'+device_name+'_BME280_0_H/config').encode()
BME280_0_CONFIG_TOPIC_P   = ('homeassistant/sensor/'+device_name+'_BME280_0_P/config').encode()
BME280_0_CONFIG_PAYLOAD_T = ('{"device_class": "temperature", "name": "'+ device_name + '_BME280_0_T", "state_topic": "homeassistant/sensor/'+device_name+'_BME280_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }').encode()
BME280_0_CONFIG_PAYLOAD_H = ('{"device_class": "humidity", "name": "'   + device_name + '_BME280_0_H", "state_topic": "homeassistant/sensor/'+device_name+'_BME280_0/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }').encode()
BME280_0_CONFIG_PAYLOAD_P = ('{"device_class": "pressure", "name": "'   + device_name + '_BME280_0_P", "state_topic": "homeassistant/sensor/'+device_name+'_BME280_0/state", "unit_of_measurement": "hPa", "value_template": "{{ value_json.pressure}}" }').encode()
BME280_0_STATE_TOPIC      = ('homeassistant/sensor/'   + device_name + '_BME280_0/state').encode()
