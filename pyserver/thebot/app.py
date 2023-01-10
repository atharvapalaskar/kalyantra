# USING MQTT PROTOCOL 
# REFER kalsh.sh and services/kalyantrapy.service to create system service

import os   
from mqtt_pubsub.handler import *
from utils import *    
from speech_rec import get_text
from kal_bot_ent import kalyantra  

# mqtt
mq_client.connect(os.getenv('MQTT_URL'), 8883)  
mq_client.on_connect = on_connect 
mq_client.on_subscribe = on_subscribe
mq_client.on_message = on_message
mq_client.on_publish = on_publish 

mq_client.subscribe(topic_en.BASE.value, qos=1) 
mq_client.subscribe(topic_en.MOVE.value, qos=1)
# mq_client.subscribe("sensor", qos=1) 
mq_client.subscribe(topic_en.PICAM.value, qos=1) 
mq_client.subscribe('movecm', qos=1)


try:

  WAKE1 = 'ok yantra'
  WAKE2 = 'do something'

  mq_client.loop_start() 

  while True:  
    
    print("listening")
    txt = get_text()
    print(txt)
    if txt != None :
      if txt.lower().count(WAKE1) > 0 or txt.lower().count(WAKE2) > 0 :
        print("found wake up")
        kalyantra.speak("Yes tell me")
        print("speak commands")
        dotxt = get_text(False)
        print(f"do: {dotxt}")
         
    
  # mq_client.loop_forever()
except KeyboardInterrupt:
  mq_client.loop_stop()
  mq_client.disconnect()
  print(f'app closed by ^C')

