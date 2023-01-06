# from pyserver.kal_bot_ent import kalyantra   
# from pyserver.mqtt_pubsub.util import mq_client    

# async def botMoves(move):  
#    try:              
#       await kalyantra.moves(move)   
#       # if kalyantra.moving == 'backward':
#       #    k = await kalyantra.sensor('back') 
#       #    if k == 0:
#       #       await kalyantra.moves('halt')
#       #       mq_client.publish("send",payload=f"backward obstacle : {k}",qos=2)
               
#    except : 
#       mq_client.publish("error", payload="undefined move", qos=2) 

           