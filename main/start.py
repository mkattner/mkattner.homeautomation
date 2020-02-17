# https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy
# https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html
# screen /dev/tty.usbmodem* 115200


import machine, time, os, globals

def mqtt_callback(topic, payload):
  global SWITCH_0_SET_TOPIC, SWITCH_0_STATE, SWITCH_0
  print("Callback: " + str(topic) + " - " + str(payload))
  
  
  if topic == SWITCH_0_SET_TOPIC:
    print('SWITCH_0_SET_TOPIC', SWITCH_0_SET_TOPIC)
    
    SWITCH_0_STATE = payload
    print(SWITCH_0_STATE)
    if SWITCH_0_STATE == b"OFF":
      SWITCH_0.on()
    elif SWITCH_0_STATE == b"ON":
      SWITCH_0.off()
    
    client.publish(SWITCH_0_STATE_TOPIC, SWITCH_0_STATE)
    

def connect_MQTT():
  global mqtt_client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password
  client = MQTTClient(mqtt_client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password)
  client.set_callback(mqtt_callback)
  client.connect()
  print("Connected")
  return client

def subscribe_MQTT(topic):
  print("subscribe_MQTT: ")
  print(topic)
  client.subscribe(topic) #subscribe just once the broker knows it
  
  



# Connect to MQTT
try:
  global client
  client = connect_MQTT()
  print("Connected to MQTT server.")
except OSError as e:
  print("ERROR: Can't connect to MQTT server.")
  globals.restart_and_reconnect()
except Exception as e:
  print("ERROR Try something.")


if globals.SWITCH_0_load == True:
  SWITCH_0 = machine.Pin(0, machine.Pin.OUT)
  SWITCH_0_SET_TOPIC      = b'homeassistant/switch/SWITCH_0/set'
  SWITCH_0_CONFIG_TOPIC   = b'homeassistant/switch/SWITCH_0/config'
  SWITCH_0_CONFIG_PAYLOAD = b'{"name": "SWITCH_0", "command_topic": "homeassistant/switch/SWITCH_0/set", "state_topic": "homeassistant/switch/SWITCH_0/state"}'
  SWITCH_0_STATE_TOPIC    = b'homeassistant/switch/SWITCH_0/state'
  SWITCH_0_STATE          = b'OFF'

  print('')
  print('PUBLISH')
  print(SWITCH_0_CONFIG_TOPIC)
  print(SWITCH_0_CONFIG_PAYLOAD)
  client.publish(SWITCH_0_CONFIG_TOPIC, SWITCH_0_CONFIG_PAYLOAD)

  print('')
  print('PUBLISH')
  print(SWITCH_0_STATE_TOPIC)
  print(SWITCH_0_STATE)
  client.publish(SWITCH_0_STATE_TOPIC, SWITCH_0_STATE)

  SWITCH_0 = machine.Pin(0, machine.Pin.OUT)

  # initialize SWITCH 
  SWITCH_0.on(); #off
  print(SWITCH_0_STATE_TOPIC + " - " + SWITCH_0_STATE)
  client.publish(SWITCH_0_STATE_TOPIC, SWITCH_0_STATE)



if globals.DS1820B_0_load == True:
  import onewire, ds18x20
  DS1820B_0_CONFIG_TOPIC   = b'homeassistant/sensor/DS1820B_0/config'
  DS1820B_0_CONFIG_PAYLOAD = b'{"device_class": "temperature", "name": "DS1820B_0_Temperature", "state_topic": "homeassistant/sensor/DS1820B_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
  DS1820B_0_STATE_TOPIC    = b'homeassistant/sensor/DS1820B_0/state'

  print('')
  print('PUBLISH')
  print(DS1820B_0_CONFIG_TOPIC)
  print(DS1820B_0_CONFIG_PAYLOAD)
  client.publish(DS1820B_0_CONFIG_TOPIC, DS1820B_0_CONFIG_PAYLOAD)

  ds_pin = machine.Pin(2)
  DS1820B = ds18x20.DS18X20(onewire.OneWire(ds_pin))

  roms = DS1820B.scan()
  print('Found DS devices: ', roms)

  DS1820B.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    print(rom)
    print(DS1820B.read_temp(rom))

  DS1820B_0 = roms[0]
  #time.sleep(5)


if globals.DHT11_0_load == True:
  import dht
  DHT11_0_CONFIG_TOPIC_T   = b'homeassistant/sensor/DHT11_0_T/config'
  DHT11_0_CONFIG_TOPIC_H   = b'homeassistant/sensor/DHT11_0_H/config'
  DHT11_0_CONFIG_PAYLOAD_T = b'{"device_class": "temperature", "name": "DHT11_0_Temperature", "state_topic": "homeassistant/sensor/DHT11_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
  DHT11_0_CONFIG_PAYLOAD_H = b'{"device_class": "humidity", "name": "DHT11_0_Humidity", "state_topic": "homeassistant/sensor/DHT11_0/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
  DHT11_0_STATE_TOPIC      = b'homeassistant/sensor/DHT11_0/state'

  print('')
  print('PUBLISH')
  print(DHT11_0_CONFIG_TOPIC_T)
  print(DHT11_0_CONFIG_PAYLOAD_T)
  client.publish(DHT11_0_CONFIG_TOPIC_T, DHT11_0_CONFIG_PAYLOAD_T)

  print('')
  print('PUBLISH')
  print(DHT11_0_CONFIG_TOPIC_H)
  print(DHT11_0_CONFIG_PAYLOAD_H)
  client.publish(DHT11_0_CONFIG_TOPIC_H, DHT11_0_CONFIG_PAYLOAD_H)

  DHT11_0 = dht.DHT11(machine.Pin(5))


if globals.BME_280_0_load == True:
  from machine import Pin, I2C
  import BME280

  i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

  globals.BME280_0 = BME280.BME280(i2c=i2c)

  
  print('')
  print('PUBLISH')
  print(globals.BME280_0_CONFIG_TOPIC_T)
  print(globals.BME280_0_CONFIG_PAYLOAD_T)
  client.publish(globals.BME280_0_CONFIG_TOPIC_T, globals.BME280_0_CONFIG_PAYLOAD_T)

  print('')
  print('PUBLISH')
  print(globals.BME280_0_CONFIG_TOPIC_H)
  print(globals.BME280_0_CONFIG_PAYLOAD_H)
  client.publish(globals.BME280_0_CONFIG_TOPIC_H, globals.BME280_0_CONFIG_PAYLOAD_H)

  print('')
  print('PUBLISH')
  print(globals.BME280_0_CONFIG_TOPIC_P)
  print(globals.BME280_0_CONFIG_PAYLOAD_P)
  client.publish(globals.BME280_0_CONFIG_TOPIC_P, globals.BME280_0_CONFIG_PAYLOAD_P)


import loop

try:

  loop.run(client)

except Exception as e:
  print("EXCEPTION in loop")
  print(e)
  globals.restart_and_reconnect()