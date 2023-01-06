import os
import firebase_admin
import paho.mqtt.client as mqtt 
from dotenv import load_dotenv  
from firebase_admin import credentials
from firebase_admin import storage   

load_dotenv() 
 
global mq_client 
mq_client = mqtt.Client(client_id="raspi", userdata=dict(username=os.getenv('MQTT_USERNAME'),client_id="raspi"), protocol=mqtt.MQTTv5)
mq_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mq_client.username_pw_set(os.getenv('MQTT_USERNAME'),os.getenv('MQTT_PASSWORD'))
 
cred = credentials.Certificate(f"{os.getcwd()}/firebase.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': str(os.getenv('FB_BUCKET'))
}) 
bucket = storage.bucket()
 
