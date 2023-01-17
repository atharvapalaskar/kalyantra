import json
import os 
import asyncio
from time import sleep
from datetime import datetime
from picamera import PiCamera 
from utils import bucket
from gpiozero import Device, Robot, DistanceSensor, DigitalInputDevice
import platform
from gpiozero.pins.mock import MockFactory
from timer_util import ResetTimer 
from enums import *  
import logging 
from datetime import datetime
import re
from utils import mq_client
import speech_recognition as sr  

logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO,)

print(str(platform.platform()).split('-')[0])
if str(platform.platform()).split('-')[0] == 'macOS':
     Device.pin_factory = MockFactory() 

class Spe_sen_cdataset(): # data for speed sensor related calculation       
    def __init__(self):
        self.wheel_steps = 20 # num of holes in the disk 
        self.wheel_steps_counter = 0  # steps counter to count steps completed for a task 
        self.wheel_diameter = 6.6
        self.wheel_circumference =  self.wheel_diameter * 3.14 # d x pi
        self.cms_per_step = self.wheel_circumference / self.wheel_steps  
        # self.speed = 0
        # self.interval = 10.0 # timer interval for calculatng RPM

class Pilot_d():
    def __init__(self) -> None:
        self.active = False
        self.cms = 0  
        self.steps_rq = 0 # steps required for a task 

class Kalyantra:
     
    def __init__(self):
        # Motor Driver Board L298N
        self.bot = Robot(left=(23,22),right=(18,17),pwm=False) 
        # Distance Sensor HC-SR04
        self.front_sensor = DistanceSensor(echo=6, trigger=5,threshold_distance=0.25)
        # IR Obstacle Sensor (Active Low)   
        self.back_sensor = DigitalInputDevice(pin=12)        
        # Speed Sensor LM393
        self.speed_sensor = DigitalInputDevice(pin=4)
        # Pi Camera (I'm using 5MP Pi Cam :( suggest to use high res cam :) )
        self.camera = PiCamera()  
        # TTS lib init (speakers connected to audio jack)
        # self.ttsen = pyttsx3.init()  deprecate using os.sys.. with espeak
        self.srecg = sr.Recognizer() 
        self.mic = sr.Microphone()#device_index=1

        # data
        self.move = 'halt' 
        self.moving = True
            #"move" is setted as main movement after obstacle (halts) bot will resume to move in "move" direction
            #"moving" current status of bot moving for  
            #moving=True->obstacle->moving=False->obstacle_cleared->moving=True
        self.frontClear = True
        self.backClear = True
        self.speed_sen_data = Spe_sen_cdataset()
        # self.speed_cal_timer = ResetTimer(None,None)
        self.pilot_data = Pilot_d() # auto pilot mode to travel certain distance
        self.current_task = '--'
        self.last_task = '--'
        
    def speak(self,text):
        
        print("speakingg ")
        os.system(f"espeak -g 6 -s 210 '{text}'") 
        
    #controls bot movement
    async def moves(self,msg:str=None,main=False,mov='halt') -> str:
        try:
            
            cms = 0    

            if msg != None:
                move = msg.split(' ')[0].strip() 
                val = int(re.findall(r'\d+', msg)[0]) if len(re.findall(r'\d+', msg)) > 0 else 0
                if msg.endswith(' m'):val = val * 100  #convert m to cm 
                cms = val
                print(f'move msg: {cms} cm') 
                print(move) 
            else:
                move = mov 

            if main: 
                self.move = move 
                self.last_task = self.current_task
                self.current_task = f'move {msg}' if msg != None else f'move {self.move}' 

            self.moving = True if move != move_en.HALT.value else False 

            if cms != 0:#if cms 
                print(f"cms given :{cms} activating pilot")
                self.speed_sen_data.wheel_steps_counter = 0     
                # convert cm to steps : no of steps required to travel a distance in centimeters
                steps_req = cms / self.speed_sen_data.cms_per_step
                print(f"steps req: {steps_req} ")
                self.pilot_data.steps_rq = steps_req
                self.pilot_data.cms = cms
                self.pilot_data.active = True
                print(f"pil: {self.pilot_data.active}") 
             

            # speakStr = ''
            match(move):
              
                case move_en.FORWARD.value: 
                    self.bot.forward() 
                    # speakStr = "Moving forward" 

                case move_en.BACKWARD.value:
                    self.bot.backward()
                    # speakStr = "Moving backward" 
                     
                case move_en.RIGHT.value:
                    self.bot.right()
                    # speakStr = "Turning right" 

                case move_en.LEFT.value:
                    self.bot.left() 
                    # speakStr = "Turning left" 

                case move_en.HALT.value:
                    self.bot.stop() 
                    # speakStr = "Halt" 

                case _:
                    raise Exception('Unkown move')
                # add uturn or 180 or turn over   
                
            mq_client.publish("task",
               payload=json.dumps({"data":{"taskName":"any","currentTask":self.current_task,"nextTask":"--","lastTask":self.last_task,"move":self.move,"moving":self.moving,"pilot":self.pilot_data.active}}),
               qos=1) 
            # self.speak(speakStr) 
                   
        except Exception as e: 
            return f"error at moves({move,main}) : {e}" 

        
    # sensor events callabacks to control movement
    def sensors_n_moves(self,*args,**kwargs): 
        senr = kwargs['sensor'] 
        evnt = kwargs['event'] 
        # print(f"sensor:{senr}, event:{evnt}") 
                        
        try:
            match(senr):
                    
                case sensors_en.FRONT:  
                    if evnt == sensors_en.DEACTIVE and self.move != 'halt' and self.move != 'backward' and self.moving :
                        self.frontClear = False
                        # print("obstacle: stoping was moving forward") 
                        mq_client.publish("sensor",payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear,}}),qos=1) 
                        asyncio.run(self.moves(mov='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move != 'halt' and self.move != 'backward':
                        self.frontClear = True
                        # print("clear: continue move forward")
                        mq_client.publish("sensor",payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear}}),qos=1) 
                        asyncio.run(self.moves(mov='forward'))
                        return

                case sensors_en.BACK:   
                    if evnt == sensors_en.DEACTIVE and self.move != 'halt' and self.move != 'forward' and self.moving :
                        self.backClear = False
                        # print("back_obstacle: stoping was moving backward")
                        mq_client.publish("sensor",payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear,}}),qos=1) 
                        asyncio.run(self.moves(mov='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move != 'halt' and self.move != 'forward' :
                        self.backClear = True
                        # print("back_clear: continue move backward")
                        mq_client.publish("sensor",payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear}}),qos=1) 
                        asyncio.run(self.moves(mov='backward'))
                        return  

                case sensors_en.SPEED:
                    # keep steps counts by sensor event and handle pilot 
                    self.speed_sen_data.wheel_steps_counter += 1
                    print(self.speed_sen_data.wheel_steps_counter)
                    if self.pilot_data.active :
                        if self.speed_sen_data.wheel_steps_counter > self.pilot_data.steps_rq :
                            print(f"pilot: done moving cms: {self.pilot_data.cms} steps: {self.pilot_data.steps_rq} ")
                            self.pilot_data.active = False 
                            asyncio.run(self.moves(mov='halt',main=True))
                            return
                        
        except Exception as e:
            print(f"err at sensors_n_moves({senr},{evnt}): {e}") 


    #click photo and upload to firebase
    async def click_pic(self): 
        try:
            file_name = f'picam_img/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.jpg'
            # print(os.getcwd())
            file_path = f"{os.getcwd()}/{file_name}"
 
            self.camera.resolution = (1024, 768)
            self.camera.start_preview()
            # capture after stablization
            sleep(1)
            self.camera.capture(file_name)
            # logging.info(f'photo captured {file_name}')
            
            # firebase
            blob = bucket.blob(file_name)
            blob.upload_from_filename(file_path) 
            return file_name
        
        except Exception as e:
            logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} err at click_pic(): {e}") 


    def speed_timer_do(self,do):
        print(f"do: {do}")
        # create the timer which will execute the method output after interval seconds
        match do:
            case 'set':
                self.speed_cal_timer = ResetTimer(self.speed_sen_data.interval, self.rpm_cal)
            case 'run':
                self.speed_cal_timer.run()
            case 'res':
                self.speed_cal_timer.reset()
            case 'canc':
                self.speed_cal_timer.cancel()
     

kalyantra = Kalyantra() 

def add_sensor_listeners():
    kalyantra.front_sensor.when_in_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.DEACTIVE)
    kalyantra.front_sensor.when_out_of_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.ACTIVE)

    kalyantra.back_sensor.when_activated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.ACTIVE)
    kalyantra.back_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.DEACTIVE)

    kalyantra.speed_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.SPEED,event=sensors_en.DEACTIVE)


# kalyantra.speed_timer_do('set')
# kalyantra.speed_timer_do('run')
 