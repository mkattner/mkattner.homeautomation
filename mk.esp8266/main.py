import machine, onewire, ds18x20, time, os
import dht

#f = open('data.txt', 'r')
#print(f.read())
#f.close()


# Complete project details at https://RandomNerdTutorials.com

global client_id

I2C_SWITCH_0 = machine.Pin(0, machine.Pin.OUT)
I2C_SWITCH_0_SET_TOPIC = b'homeassistant/switch/I2C_SWITCH_0/set'
I2C_SWITCH_0_CONFIG_TOPIC = b'homeassistant/switch/I2C_SWITCH_0/config'
I2C_SWITCH_0_CONFIG_PAYLOAD = b'{"name": "I2C switch 0", "command_topic": "homeassistant/switch/I2C_SWITCH_0/set", "state_topic": "homeassistant/switch/I2C_SWITCH_0/state"}'
I2C_SWITCH_0_STATE_TOPIC = b'homeassistant/switch/I2C_SWITCH_0/state'
I2C_SWITCH_0_STATE = b'OFF'

# I2C_BINARY_0


DS1820B_0_CONFIG_TOPIC = b'homeassistant/sensor/DS1820B_0/config'
DS1820B_0_CONFIG_PAYLOAD = b'{"device_class": "temperature", "name": "DS1820B_0", "state_topic": "homeassistant/sensor/DS1820B_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
DS1820B_0_STATE_TOPIC = b'homeassistant/sensor/DS1820B_0/state'

DHT11_0_CONFIG_TOPIC_T = b'homeassistant/sensor/DHT11_0_T/config'
DHT11_0_CONFIG_TOPIC_H = b'homeassistant/sensor/DHT11_0_H/config'
DHT11_0_CONFIG_PAYLOAD_T = b'{"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/DHT11_0/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
DHT11_0_CONFIG_PAYLOAD_H = b'{"device_class": "humidity", "name": "Humidity", "state_topic": "homeassistant/sensor/DHT11_0/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
DHT11_0_STATE_TOPIC = b'homeassistant/sensor/DHT11_0/state'


def sub_cb(topic, payload):
  global I2C_SWITCH_0_SET_TOPIC, I2C_SWITCH_0_STATE, I2C_SWITCH_0
  print("Callback: " + str(topic) + " - " + str(payload))
  
  
  if topic == I2C_SWITCH_0_SET_TOPIC:
    print('I2C_SWITCH_0_SET_TOPIC', I2C_SWITCH_0_SET_TOPIC)
    
    I2C_SWITCH_0_STATE = payload
    print(I2C_SWITCH_0_STATE)
    if I2C_SWITCH_0_STATE == b"OFF":
      I2C_SWITCH_0.on()
    elif I2C_SWITCH_0_STATE == b"ON":
      I2C_SWITCH_0.off()
    
    client.publish(I2C_SWITCH_0_STATE_TOPIC, I2C_SWITCH_0_STATE)
    

def connect():
  global client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password
  client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password)
  client.set_callback(sub_cb)
  client.connect()
  print("Connected")
  return client

def subscribe(topic):
  print("subscribe:")
  print(topic)
  client.subscribe(topic) #subscribe just once the broker knows it
  
  

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect()
  
  try:
   #topic_sub = b'homeassistant/msg/2'
   #subscribe(topic_sub)
   
   subscribe(I2C_SWITCH_0_SET_TOPIC)
   
  except Exception as e:
    print(e)
except OSError as e:
  restart_and_reconnect()
except Exception as e:
  print("ERROR Try something")


#msg = b''
#print("publish:")
#print(I2C_SWITCH_0_CONFIG_TOPIC)
#print(msg)
#client.publish(I2C_SWITCH_0_CONFIG_TOPIC, msg)

print("publish: config")
print(I2C_SWITCH_0_CONFIG_TOPIC)
print(I2C_SWITCH_0_CONFIG_PAYLOAD)
client.publish(I2C_SWITCH_0_CONFIG_TOPIC, I2C_SWITCH_0_CONFIG_PAYLOAD)

print("publish:")
print(I2C_SWITCH_0_STATE_TOPIC)
print(I2C_SWITCH_0_STATE)
client.publish(I2C_SWITCH_0_STATE_TOPIC, I2C_SWITCH_0_STATE)


print("publish: config")
print(DS1820B_0_CONFIG_TOPIC)
print(DS1820B_0_CONFIG_PAYLOAD)
client.publish(DS1820B_0_CONFIG_TOPIC, DS1820B_0_CONFIG_PAYLOAD)


print("publish: config")
print(DHT11_0_CONFIG_TOPIC_T)
print(DHT11_0_CONFIG_PAYLOAD_T)
client.publish(DHT11_0_CONFIG_TOPIC_T, DHT11_0_CONFIG_PAYLOAD_T)

print(DHT11_0_CONFIG_TOPIC_H)
print(DHT11_0_CONFIG_PAYLOAD_H)
client.publish(DHT11_0_CONFIG_TOPIC_H, DHT11_0_CONFIG_PAYLOAD_H)


#msg=b'{ "temperature": 23.20}'
#print(DS1820B_0_STATE_TOPIC)
#print(msg)
#client.publish(DS1820B_0_STATE_TOPIC,msg)


ds_pin = machine.Pin(4)
DS1820B = ds18x20.DS18X20(onewire.OneWire(ds_pin))

DHT11_0 = dht.DHT11(machine.Pin(5))

roms = DS1820B.scan()
print('Found DS devices: ', roms)

DS1820B.convert_temp()
time.sleep_ms(750)
for rom in roms:
  print(rom)
  print(DS1820B.read_temp(rom))
#time.sleep(5)

I2C_SWITCH_0 = machine.Pin(0, machine.Pin.OUT)

# initialize I2C_SWITCH 
I2C_SWITCH_0.on(); #off
print(I2C_SWITCH_0_STATE_TOPIC + " - " + I2C_SWITCH_0_STATE)
client.publish(I2C_SWITCH_0_STATE_TOPIC, I2C_SWITCH_0_STATE)

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
    DS1820B_0 = roms[0]
    
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
      
      print(I2C_SWITCH_0_STATE)
      
      
      
      # I2C_SWITCH state update
      value = I2C_SWITCH_0.value()
      if value == 0:
        I2C_SWITCH_0_STATE = b"ON"
      elif value == 1:
        I2C_SWITCH_0_STATE = b"OFF"
      print(I2C_SWITCH_0_STATE_TOPIC + " - " + I2C_SWITCH_0_STATE)
      client.publish(I2C_SWITCH_0_STATE_TOPIC, I2C_SWITCH_0_STATE)
      
      last_message_5s = time.time()
      
    if (time.time() - last_message_10s) > 10:
      # ________________________
      #     every 10 seconds
      # ------------------------
      print("every 10 seconds");
      
      # ---
      
      # DS1820B update
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
      DHT11_0.measure()
      DHT11_0_msg = '{ "temperature":' + str(DHT11_0.temperature()) + ', "humidity":' + str(DHT11_0.humidity()) + '}'
      print(DHT11_0_msg)
      client.publish(DHT11_0_STATE_TOPIC, DHT11_0_msg)
      
      # ---
      
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
