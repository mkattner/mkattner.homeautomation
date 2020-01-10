import time, globals




def run(client):
  last_message_1s   = 0
  last_message_5s   = 0
  last_message_10s  = 0
  last_message_20s  = 0
  last_message_30s  = 0
  last_message_60s  = 0
  last_message_300s = 0
  last_message_600s = 0

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

        # --- end 1 second
        last_message_1s = time.time()
      
      if (time.time() - last_message_5s) > 5:
        # ________________________
        #     every 5 seconds
        # ------------------------
        print("every 5 seconds")
        

        if globals.SWITCH_0_load == True:
          print(SWITCH_0_STATE)
          # SWITCH state update
          value = SWITCH_0.value()
          if value == 0:
            SWITCH_0_STATE = b"ON"
          elif value == 1:
            SWITCH_0_STATE = b"OFF"
          print(SWITCH_0_STATE_TOPIC + " - " + SWITCH_0_STATE)
          client.publish(SWITCH_0_STATE_TOPIC, SWITCH_0_STATE)
        
        # --- end 5 second
        last_message_5s = time.time()
        
      if (time.time() - last_message_10s) > 10:
        # ________________________
        #     every 10 seconds
        # ------------------------
        print("every 10 seconds");

        # --- end 10 second
        last_message_10s = time.time()
        
      if (time.time() - last_message_20s) > 20:
        # ________________________
        #     every 20 seconds
        # ------------------------
        print("every 20 seconds");

        # --- end 20 second
        last_message_20s = time.time()
        
      if (time.time() - last_message_30s) > 30:
        # ________________________
        #     every 30 seconds
        # ------------------------
        print("every 30 seconds");

        # --- end 30 second
        last_message_30s = time.time()
        
      if (time.time() - last_message_60s) > 60:
        # ________________________
        #     every 60 seconds
        # ------------------------
        print("every 60 seconds");


        # DS1820B update
        if globals.DS1820B_0_load == True:
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
        if globals.DHT11_0_load == True:
          DHT11_0.measure()
          DHT11_0_msg = '{ "temperature":' + str(DHT11_0.temperature()) + ', "humidity":' + str(DHT11_0.humidity()) + '}'
          print(DHT11_0_msg)
          client.publish(DHT11_0_STATE_TOPIC, DHT11_0_msg)
        
        # ---
        
        #BME280 update
        if globals.BME_280_0_load == True:
          
          BME280_0_msg = '{ "temperature":' + globals.BME280_0.raw_temperature + ', "humidity":' + globals.BME280_0.raw_humidity + ', "pressure":' + globals.BME280_0.raw_pressure + '}'
          #BME280_0_msg = '{ "temperature":3, "humidity":4, "pressure":5}'
          print(BME280_0_msg)
          client.publish(globals.BME280_0_STATE_TOPIC, BME280_0_msg)


        # --- end 60 second
        last_message_60s = time.time()  
        
      if (time.time() - last_message_300s) > 300:
        # ________________________
        #     every 300 seconds
        # ------------------------
        print("every 300 seconds");
        
        # --- end 300 second
        last_message_300s = time.time()   
      
      if (time.time() - last_message_600s) > 600:
        # ________________________
        #     every 600 seconds
        # ------------------------
        print("every 600 seconds");
        
        # --- end 600 second
        last_message_600s = time.time()
      
    except Exception as e:
      print("EXCEPTION in loop")
      print(e)
      globals.restart_and_reconnect()
