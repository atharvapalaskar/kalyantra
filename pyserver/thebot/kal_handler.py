import asyncio
from enums import *
from utils import mq_client 
from kal_bot_ent import kalyantra      
import json

def handler(topic,msg,by='app'): 
    print(f'handler({topic},{by}):{msg}')
    match(topic):

        case sub_topic_en.BASE.value:
            print(msg) 
            kalyantra.speak("check")
            mq_client.publish(pub_topic_en.STATUS.value,payload=json.dumps({"data":"ready"}),qos=1)
            return

        case sub_topic_en.MOVE.value: 
            asyncio.run(kalyantra.moves(msg=msg,main=True))  
            print("done")
            # mq_client.publish("acks",payload=f"moving: {msg} started",qos=1)
            return
            
        case sub_topic_en.VCMD.value: 
            kalyantra.tasks_creator(msg=msg) 
            # o = asyncio.run(kalyantra.sensor(use=msg.payload.decode('UTF-8')))
            # mq_client.publish("send",payload=f"data: {o}",qos=2) 
            return 
        
        case sub_topic_en.PICAM.value:
            match (msg): 
                case 'click':
                    asyncio.run(kalyantra.click_pic())  
                    # mq_client.publish(pub_topic_en.ACKS.value,payload=f"uploaded: {dt}" if dt != None else f'caut:busy',qos=1)                     
                case _:
                    print(msg)
 
        case _:
            mq_client.publish(pub_topic_en.ERR.value,payload=f"unhandled topic:{topic} msg:{msg}",qos=1) 
            return 
 
 


 