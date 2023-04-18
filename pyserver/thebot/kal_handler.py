import asyncio
from enums import *
from utils import mq_client 
from kal_bot_ent import kalyantra      
import json

def handler(topic,msg,by='in_mic'): 
    print(f'handler({topic},{by}):{msg}')
    match(topic):

        case sub_topic_en.BASE.value: 
            kalyantra.speak("check")
            mq_client.publish(pub_topic_en.STATUS.value,payload=json.dumps({"data":"ready"}),qos=1)
            return

        case sub_topic_en.MOVE.value: 
            kalyantra.task_name = msg
            asyncio.run(kalyantra.moves(msg=msg,main=True))   
            return
            
        case sub_topic_en.VCMD.value: 
            kalyantra.task_name = msg  
            kalyantra.tasks_creator(msg=msg)  
            return 
        
        case sub_topic_en.PICAM.value:
            kalyantra.task_name = msg
            asyncio.run(kalyantra.click_pic(msg=msg))         
 
        case _:
            mq_client.publish(pub_topic_en.ERR.value,payload=f"unhandled topic:{topic} msg:{msg}",qos=1) 
            return 
 
 


 