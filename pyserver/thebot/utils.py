import os
import firebase_admin
import paho.mqtt.client as mqtt 
from dotenv import load_dotenv  
from firebase_admin import credentials
from firebase_admin import storage    
import ssl
# import logging

# logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO)

load_dotenv()   

# mqtt
global mq_client 

mq_client = mqtt.Client(client_id=os.getenv('MQTT_CLIENT_ID'),userdata=dict(client_id=os.getenv('MQTT_CLIENT_ID')),protocol=mqtt.MQTTv5)
mq_client.tls_set(os.getenv('CA_ROOT_CERT_FILE'),certfile=os.getenv('THING_CERT_FILE'),keyfile=os.getenv('THING_PRIVATE_KEY'), cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
  
# firebase
cred = credentials.Certificate(f"{os.getcwd()}/firebase.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': str(os.getenv('FB_BUCKET'))
}) 
bucket = storage.bucket()
  