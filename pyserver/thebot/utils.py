import os
import firebase_admin
import paho.mqtt.client as mqtt 
from dotenv import load_dotenv  
from firebase_admin import credentials
from firebase_admin import storage    
# import logging

# logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO)

load_dotenv()  

# mqtt
global mq_client 
mq_client = mqtt.Client(client_id=f"{os.getenv('MQTT_USERNAME')}raspi", userdata=dict(username=os.getenv('MQTT_USERNAME'),client_id=f"{os.getenv('MQTT_USERNAME')}raspi"), protocol=mqtt.MQTTv5)
mq_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mq_client.username_pw_set(os.getenv('MQTT_USERNAME'),os.getenv('MQTT_PASSWORD'))
 
# firebase
cred = credentials.Certificate(f"{os.getcwd()}/firebase.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': str(os.getenv('FB_BUCKET'))
}) 
bucket = storage.bucket()
 
