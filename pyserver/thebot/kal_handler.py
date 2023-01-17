import asyncio
from utils import mq_client 
from kal_bot_ent import kalyantra      
from enums import topic_en
import json

def handler(topic,msg,by='app'): 
    print(f'handler({topic},{by}):{msg}')
    match(topic):

        case topic_en.BASE.value:
            print(msg) 
            kalyantra.speak("check")
            mq_client.publish("status",payload=json.dumps({"data":"ready"}),qos=1)
            return

        case topic_en.MOVE.value: 
            asyncio.run(kalyantra.moves(msg=msg,main=True))  
            print("done")
            # mq_client.publish("acks",payload=f"moving: {msg} started",qos=1)
            return
            
        # case 'sensor':
        #     o = asyncio.run(kalyantra.sensor(use=msg.payload.decode('UTF-8')))
        #     mq_client.publish("send",payload=f"data: {o}",qos=2) 
        #     return 
        
        case topic_en.PICAM.value:
            match (msg): 
                case 'click':
                    dt = asyncio.run(kalyantra.click_pic()) 
                    mq_client.publish("acks",payload=f"uploaded: {dt}",qos=1) 
                case _:
                    print(msg)
 
        case _:
            mq_client.publish("error",payload=f"unhandled topic:{topic} msg:{msg}",qos=1) 
            return
 
 


 