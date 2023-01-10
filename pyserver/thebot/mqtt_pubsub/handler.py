import asyncio
from utils import mq_client 
from kal_bot_ent import kalyantra      
from enums import topic_en

def on_connect(mq_client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    print(f"Connected to mqtt client with {userdata}")
    kalyantra.speak("Namas te, I am Ready") 

def on_publish(client, userdata, mid, properties=None):
    print(f"Pubmid: {mid}")
 
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Submid: {mid}")
 
def on_message(client, userdata, msg):
    print(f"got a msg -> topic: {msg.topic}" )
    match(msg.topic):

        case topic_en.BASE.value:
            print(msg.payload) 
            kalyantra.speak("check")
            return

        case topic_en.MOVE.value: 
            asyncio.run(kalyantra.moves(move=msg.payload.decode('UTF-8'),main=True))  
            mq_client.publish("acks",payload=f"moving: {msg.payload.decode('UTF-8')} started",qos=2)
            return
            
        # case 'sensor':
        #     o = asyncio.run(kalyantra.sensor(use=msg.payload.decode('UTF-8')))
        #     mq_client.publish("send",payload=f"data: {o}",qos=2) 
        #     return 
        
        case topic_en.PICAM.value:
            match (msg.payload.decode('UTF-8')): 
                case 'click':
                    dt = asyncio.run(kalyantra.click_pic()) 
                    mq_client.publish("acks",payload=f"uploaded: {dt}",qos=2) 
                case _:
                    print(msg.payload.decode('UTF-8'))

        #  temp topic
        case 'movecm': 
            asyncio.run(kalyantra.moves(move=msg.payload.decode('UTF-8'),main=True,cms=10))  
            mq_client.publish("acks",payload=f"moving: {msg.payload.decode('UTF-8')} completed",qos=2)
            return

        case _:
            mq_client.publish("error",payload=f"got a message at unhandled topic",qos=2) 
            return
 
 


 