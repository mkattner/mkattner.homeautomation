# https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy
# https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html
# screen /dev/tty.usbmodem* 115200


import machine, time, os

def sub_cb(topic, payload):
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
  client.set_callback(sub_cb)
  client.connect()
  print("Connected")
  return client

def subscribe_MQTT(topic):
  print("subscribe_MQTT: ")
  print(topic)
  client.subscribe(topic) #subscribe just once the broker knows it
  
  

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

# Connect to MQTT
try:
  client = connect_MQTT()
  print("Connected to MQTT server.")
except OSError as e:
  print("ERROR: Can't connect to MQTT server.")
  restart_and_reconnect()
except Exception as e:
  print("ERROR Try something.")

SWITCH_0_load = False
if SWITCH_0_load == True:
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


DS1820B_0_load = True
if DS1820B_0_load == True:
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

DHT11_0_load = False
if DHT11_0_load == True:
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

BME_280_0_load = True
if BME_280_0_load == True:
  from machine import Pin, I2C
  import BME280

  i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

  bme = BME280.BME280(i2c=i2c)
  temp = bme.raw_temperature
  hum = bme.raw_humidity
  pres = bme.raw_pressure

  print('Temperature: ', temp)
  print('Humidity: ', hum)
  print('Pressure: ', pres)

  BME280_0_CONFIG_TOPIC_T   = b'homeassistant/sensor/BME280_0_T/config'
  BME280_0_CONFIG_TOPIC_H   = b'homeassistant/sensor/BME280_0_H/config'
  BME280_0_CONFIG_TOPIC_P   = b'homeassistant/sensor/BME280_0_P/config'
  BME280_0_CONFIG_PAYLOAD_T = b'{"device_class": "temperature", "name": "BME280_0_Temperature", "state_topic": "homeassistant/sensor/BME280_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
  BME280_0_CONFIG_PAYLOAD_H = b'{"device_class": "humidity", "name": "BME280_0_Humidity", "state_topic": "homeassistant/sensor/BME280_0/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
  BME280_0_CONFIG_PAYLOAD_P = b'{"device_class": "pressure", "name": "BME280_0_Pressure", "state_topic": "homeassistant/sensor/BME280_0/state", "unit_of_measurement": "hPa", "value_template": "{{ value_json.pressure}}" }'
  BME280_0_STATE_TOPIC      = b'homeassistant/sensor/BME280_0/state'

  print('')
  print('PUBLISH')
  print(BME280_0_CONFIG_TOPIC_T)
  print(BME280_0_CONFIG_PAYLOAD_T)
  client.publish(BME280_0_CONFIG_TOPIC_T, BME280_0_CONFIG_PAYLOAD_T)

  print('')
  print('PUBLISH')
  print(BME280_0_CONFIG_TOPIC_H)
  print(BME280_0_CONFIG_PAYLOAD_H)
  client.publish(BME280_0_CONFIG_TOPIC_H, BME280_0_CONFIG_PAYLOAD_H)

  print('')
  print('PUBLISH')
  print(BME280_0_CONFIG_TOPIC_P)
  print(BME280_0_CONFIG_PAYLOAD_P)
  client.publish(BME280_0_CONFIG_TOPIC_P, BME280_0_CONFIG_PAYLOAD_P)
  

last_message_1s = 0
last_message_5s = 0
last_message_10s = 0
last_message_20s = 0
last_message_30s = 0
last_message_60s = 0


while True:
  # inizialize
  DS1820B_0_temp = 0
  try:
    
    
    client.check_msg()
    
    if (time.time() - last_message_1s) > 1:
      # ________________________
      #     every 1 second
      # ------------------------
      print("every 1 second")
      last_message_1s = time.time()
    
    elif (time.time() - last_message_5s) > 5:
      # ________________________
      #     every 5 seconds
      # ------------------------
      print("every 5 seconds")
      

      if SWITCH_0_load == True:
        print(SWITCH_0_STATE)
        # SWITCH state update
        value = SWITCH_0.value()
        if value == 0:
          SWITCH_0_STATE = b"ON"
        elif value == 1:
          SWITCH_0_STATE = b"OFF"
        print(SWITCH_0_STATE_TOPIC + " - " + SWITCH_0_STATE)
        client.publish(SWITCH_0_STATE_TOPIC, SWITCH_0_STATE)
      
      last_message_5s = time.time()
      
    if (time.time() - last_message_10s) > 10:
      # ________________________
      #     every 10 seconds
      # ------------------------
      print("every 10 seconds");
      last_message_10s = time.time()
      
    if (time.time() - last_message_20s) > 20:
      # ________________________
      #     every 20 seconds
      # ------------------------
      print("every 20 seconds");
      last_message_20s = time.time()
      
    if (time.time() - last_message_30s) > 30:
      # ________________________
      #     every 30 seconds
      # ------------------------
      print("every 30 seconds");
      last_message_30s = time.time()
      
    if (time.time() - last_message_60s) > 60:
      # ________________________
      #     every 60 seconds
      # ------------------------
      print("every 60 seconds");


      # DS1820B update
      if DS1820B_0_load == True:
        DS1820B.convert_temp()
        time.sleep_ms(750) #Note that you must execute the convert_temp() function to initiate a temperature reading, then wait at least 750ms before reading the value.
        if  DS1820B_0_temp != round(DS1820B.read_temp(DS1820B_0), 1):
          DS1820B_0_temp = round(DS1820B.read_temp(DS1820B_0), 1)
          print(DS1820B_0_temp)
          DS1820B_0_msg = '{ "temperature":' + str(DS1820B_0_temp) + '}'
          print(DS1820B_0_msg)
          client.publish(DS1820B_0_STATE_TOPIC, DS1820B_0_msg)
      
      # ---
      
      # DHT11 update
      if DHT11_0_load == True:
        DHT11_0.measure()
        DHT11_0_msg = '{ "temperature":' + str(DHT11_0.temperature()) + ', "humidity":' + str(DHT11_0.humidity()) + '}'
        print(DHT11_0_msg)
        client.publish(DHT11_0_STATE_TOPIC, DHT11_0_msg)
      
      # ---
      
      #BME280 update
      if BME_280_0_load == True:
        BME280_0_msg = '{ "temperature":' + bme.raw_temperature + ', "humidity":' + bme.raw_humidity + ', "pressure":' + bme.raw_pressure + '}'
        print(BME280_0_msg)
        client.publish(BME280_0_STATE_TOPIC, BME280_0_msg)


      last_message_60s = time.time()
      
  except OSError as e:
    print(e)
    #f = open('data.txt', 'w')
    #f.write(e)
    #f.close()
    restart_and_reconnect()
    
  except Exception as e:
    print("Strange error")
    print(e)
    restart_and_reconnect()
