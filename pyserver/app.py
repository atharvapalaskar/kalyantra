import os
from flask import Flask
# import time  
from routes import base,moves

app = Flask(__name__)

app.register_blueprint(base) 
app.register_blueprint(moves)
 
