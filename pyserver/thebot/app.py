# USING MQTT PROTOCOL 
# REFER kalsh.sh and services/kalyantrapy.service to create system service

import math
import os
import re
from kal_bot_ent import add_sensor_listeners    
from utils import *    
from speech_rec import get_text
from mqtt_events import *  
from enums import * 
import asyncio
from time import sleep
 
wake_cmds = ['ok yantra','do something','okay yantra','hey robo']

# Connect with MQTT Broker 
mq_client.on_connect = on_connect 
mq_client.on_subscribe = on_subscribe
mq_client.on_message = on_message
mq_client.on_publish = on_publish  

async def mqtt_sub_topics():  
    sleep(1) #required cause sometimes subs won't work with AWS without a cold sec after connection
    mq_client.subscribe(sub_topic_en.BASE.value) 
    mq_client.subscribe(sub_topic_en.MOVE.value) 
    mq_client.subscribe(sub_topic_en.PICAM.value)    
    mq_client.subscribe(sub_topic_en.VCMD.value)    
 
try:

  add_sensor_listeners()
  print("Connecting...")
  mq_client.connect(os.getenv('MQTT_HOST'), 8883, 45) 
  asyncio.run(mqtt_sub_topics())
  mq_client.publish(pub_topic_en.ACKS.value,f"client {os.getenv('MQTT_CLIENT_ID')} connected")
  mq_client.loop_start() 

  while True:  
     
    print("listening")
    txt = get_text()
    kalyantra.awaiting_awake_cmd = False
    kalyantra.led_handler()
    # print(txt)

    if txt != None:
      if txt.lower().count(wake_cmds[0]) > 0 or txt.lower().count(wake_cmds[1]) > 0 or txt.lower().count(wake_cmds[2]) > 0 or txt.lower().count(wake_cmds[3]) > 0:
        if kalyantra.moving:
            # halt
            asyncio.run(kalyantra.moves(msg='halt'))
            y_n = get_text(False,dur=3,interupt=True)  
            kalyantra.listening_wtd = False
            kalyantra.led_handler() 
            if y_n != None and y_n.startswith('yes'):  
               logging.info(f'({y_n})')
               kalyantra.speak('Humans are so fickel minded')
               kalyantra.moves(msg='halt',main=True) 
              #to-do ===> # or perform return <===
            # resume moving 
            else : asyncio.run(kalyantra.moves(resume=True))
        else:
            dotxt = get_text(False) 
            kalyantra.listening_wtd = False
            kalyantra.led_handler() 
            if dotxt != None: 
                
              # to-do this is for basic ideation ===>
                  # :Integrate: 
                  #  1. GPT APIs
                  #  2. for simple calculation don't use API's (will cost unnecessarily for basic calcs) 
                      # **and instead of 3rd party/ per-trained model Can try to build own NLP*,DL*,NN* model
                      # for such questions as sums won't be limited to two numbers, need to support more than limited questions sets 
                      # and should not be limited to one operation till then...
                if dotxt.startswith('calculate'): 
                    mathPrblm = dotxt 
                    soln = "out of my expertise"
                    try:
                      if 'power' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) ** int(re.findall(r'\d+', mathPrblm)[1]))       
                      elif 'times' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) * int(re.findall(r'\d+', mathPrblm)[1]))        
                      elif 'plus' or '+' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) + int(re.findall(r'\d+', mathPrblm)[1]))        
                      elif 'minus' or '-' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) - int(re.findall(r'\d+', mathPrblm)[1]))        
                      elif 'divide' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) / int(re.findall(r'\d+', mathPrblm)[1]))         
                      elif 'cube' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) ** 3)          
                      elif 'square' in mathPrblm:
                          soln = (int(re.findall(r'\d+', mathPrblm)[0]) ** 2)        
                      elif 'root' in mathPrblm:
                          soln = math.sqrt(int(re.findall(r'\d+', mathPrblm)[0]))  
                      else: raise 'not supported'
                    except Exception as e:
                        print(f'mathPrblm({mathPrblm}) e:{e}')
                    kalyantra.speak(soln)

                elif dotxt.startswith('what'):
                    soln = "out of my expertise"
                    try:
                        if 'time' in dotxt:
                           soln = datetime.now().strftime("%H:%M")
                        elif 'date' in dotxt:
                          soln = datetime.now().strftime("%d-%m-%Y")
                    except Exception as e:
                        print(f'mathPrblm({mathPrblm}) e:{e}')
                    kalyantra.speak(soln) 
              # <===

                else: kalyantra.tasks_creator(msg=dotxt)
              
  
  # mq_client.loop_forever() 
except KeyboardInterrupt:
  kalyantra.led.off()
  mq_client.loop_stop()
  mq_client.disconnect()
  print(f'app closed by ^C')

except Exception as e:
  kalyantra.led.off()
  logging.info(f'app closed with err: {e}')
 
