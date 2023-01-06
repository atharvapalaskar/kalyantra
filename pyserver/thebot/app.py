# USING MQTT PROTOCOL 
# REFER kalsh.sh and services/kalyantrapy.service to create system service

import os   
from mqtt_pubsub.handler import *
from utils import *    
 
# mqtt
mq_client.connect(os.getenv('MQTT_URL'), 8883)  
mq_client.on_connect = on_connect 
mq_client.on_subscribe = on_subscribe
mq_client.on_message = on_message
mq_client.on_publish = on_publish 

mq_client.subscribe("base", qos=1) 
mq_client.subscribe("move", qos=1)
mq_client.subscribe("sensor", qos=1) 
mq_client.subscribe("picam", qos=1) 
mq_client.loop_forever()

