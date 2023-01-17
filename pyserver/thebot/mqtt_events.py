from kal_bot_ent import kalyantra  
from kal_handler import handler     
import logging 
from datetime import datetime

logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO,)


def on_connect(mq_client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Connected to mqtt client with {userdata}") 
    kalyantra.speak("Namas te, I am Ready") 

def on_publish(client, userdata, mid, properties=None):
    print(f"fhghcgh clien : {client}, ud:{userdata}  Pubmid: {mid}")
 
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Submid: {mid}")
 
def on_message(client, userdata, msg):
    print(f"got a msg -> topic: {msg.topic}" )
    handler(topic=msg.topic,msg=msg.payload.decode('UTF-8'))
    
 