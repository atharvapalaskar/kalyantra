# USING MQTT PROTOCOL 
# REFER kalsh.sh and services/kalyantrapy.service to create system service

import os
from kal_bot_ent import add_sensor_listeners    
from utils import *    
from speech_rec import get_text
from mqtt_events import *  
from enums import * 
import asyncio
from time import sleep


WAKE1 = 'ok yantra'
WAKE2 = 'do something'
WAKE3 = 'okay yantra'

# Connect with MQTT Broker 
mq_client.on_connect = on_connect 
mq_client.on_subscribe = on_subscribe
mq_client.on_message = on_message
mq_client.on_publish = on_publish  

async def mqtt_sub_topics():  
    sleep(1) #sometimes subs won't work with AWS without a cold sec after connection
    mq_client.subscribe(sub_topic_en.BASE.value) 
    mq_client.subscribe(sub_topic_en.MOVE.value) 
    mq_client.subscribe(sub_topic_en.PICAM.value)    
    mq_client.subscribe(sub_topic_en.VCMD.value)    
 
try:

  add_sensor_listeners()
  print("Connecting")
  mq_client.connect(os.getenv('MQTT_HOST'), 8883, 45) 
  asyncio.run(mqtt_sub_topics())
  mq_client.publish(pub_topic_en.ACKS.value,f"client {os.getenv('MQTT_CLIENT_ID')} connected")
  mq_client.loop_start() 

  while True:  
    
    print("listening")
    txt = get_text()
    print(txt)
    if txt != None :
      if txt.lower().count(WAKE1) > 0 or txt.lower().count(WAKE2) > 0 or txt.lower().count(WAKE3) > 0:
        # print("found wake up")   
        dotxt = get_text(False)

        if dotxt == None: 
          print("no tasks")
        else:  
          dotxt = dotxt.lower()
          print(f"do: {dotxt}") 
          if dotxt.count('then') > 0: 
            and_split = dotxt.split('and')
            tasks = and_split[0].split('then')
            tasks.append(and_split[1])  
          elif dotxt.count('and') > 0:
            tasks = dotxt.split('and')
          else: 
            tasks = [dotxt]
                  
          for task in tasks: 
              task = task.strip()
              print(task) 
              topic= sub_topic_en.MOVE.value if task.startswith('move') else sub_topic_en.PICAM.value if task.startswith('click') else sub_topic_en.MOVE.value if task.startswith('return') else 'none'
              msg= task.split(' ')
              msg.pop(0)
              msg=' '.join(msg)
              print(f'msg: {msg}')
              # handler(topic=topic,msg=msg,by='wake')
          
          # print("all tasks done") 
  
  # mq_client.loop_forever()
except KeyboardInterrupt:
  mq_client.loop_stop()
  mq_client.disconnect()
  print(f'app closed by ^C')
 
