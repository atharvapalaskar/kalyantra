import os
import pyttsx3  
import asyncio
from time import sleep
from datetime import datetime
from picamera import PiCamera
from utils import bucket
from gpiozero import Device,Robot,DistanceSensor, DigitalInputDevice
import platform
from gpiozero.pins.mock import MockFactory
# import jsonpickle

print(str(platform.platform()).split('-')[0])
if str(platform.platform()).split('-')[0] == 'macOS':
     Device.pin_factory = MockFactory()


class Kalyantra:
     
    def __init__(self):
        # Motor Board LM..
        self.bot = Robot(left=(23,22),right=(18,17),pwm=False) 
        # IR Sensor
        # GPIO.setmode(GPIO.BCM)        
        self.back_sensor = DigitalInputDevice(pin=12) #GPIO.setup(12,GPIO.IN) #InputDevice(pin=12).
        # Distacne Sensor HC-SR04
        self.front_sensor = DistanceSensor(echo=6, trigger=5)
        # Speed Sensor
        # speed_sensor = InputDevice(pin=3)
        # Pi Camera (using 5MP Pi Cam :( :/ )
        self.camera = PiCamera() 
        # TTS (speakers connected to audio jack)
        self.ttsen = pyttsx3.init()  
       
        # data
        self.moving = 'halt'

    async def moves(self,move) -> str:
        try:

            match(move):
                    
                case 'forward':
                    self.moving = 'forward'
                    self.bot.forward()
                    self.speak("Moving forward")
                    return "done"              

                case 'backward':
                    self.moving = 'backward'
                    self.bot.backward()
                    self.speak("Moving backward")
                    return "done" 
                     
                case 'right':
                    self.moving = 'right'
                    self.bot.right()
                    self.speak("Turning right")
                    return "done"

                case 'left':
                    self.moving = 'left'
                    self.bot.left() 
                    self.speak("Turning left")
                    return "done"

                case 'halt':
                    self.moving = 'halt'
                    self.bot.stop() 
                    self.speak("Halt")
                    return "done"

                case _:
                    raise Exception("unknown move")
                    
        except : 
            return "err" 

    
    async def click_pic(self): 
        try:
            file_name = f'picam_img/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.jpg'
            # print(os.getcwd())
            file_path = f"{os.getcwd()}/{file_name}"

            self.camera.resolution = (1024, 768)
            self.camera.start_preview()

            sleep(1)
            self.camera.capture(file_name)
                
            blob = bucket.blob(file_name)
            blob.upload_from_filename(file_path)
            return file_name
        except:
            print("err occ") 

        
    def speak(self,text):
        self.ttsen.say(str(text))
        self.ttsen.runAndWait() 
 
    
    #...... 
    async def sensor(self,use,data):
        try:

            match(use):
                    
                case 'back': 
                    while True:  
                        k = self.back_sensor.value 
                        if k == 0: 
                            print("SAfa")
                            break
                    if k == 0: 
                        return k 

                # case 'front':
                    # back_sensor = InputDevice(pin=12) 
                    # while True:  
                    #     k = back_sensor.value 
                    #     if k == 0: 
                    #         print("SAfa")
                    #         break
                    # if k == 0:
                    #     return k

                case _:
                   raise Exception("unknown sensor")
                        
        except :
            return "err" 
    

    def backblock(self,pin):  
        print(f"rpi event hit back sen {pin}") 
        if self.moving == 'backward':
            print("stooping was moving backward")
            asyncio.run(self.moves(move='halt'))
            return
     
    def backs_act():
        print(f"zero event hit back act") 

    def backs_dact(self,exdata):
        print(f"zero event dect {exdata}") 
        if self.moving == 'backward':
            print("stooping was moving backward")
            asyncio.run(self.moves(move='halt'))
            return
     


kalyantra = Kalyantra()

# kalyantra.back_sensor.when_activated = kalyantra.backs_act
kalyantra.back_sensor.when_deactivated = kalyantra.backs_dact


# # eventlistener usage with RPi.GPIO
# # setup pin in kal.. class->
#     GPIO.setmode(GPIO.BCM)        
#     self.back_sensor = GPIO.setup(12,GPIO.IN)  
# # at main add listener->
#     GPIO.add_event_detect(12, GPIO.FALLING, kalyantra.backblock)