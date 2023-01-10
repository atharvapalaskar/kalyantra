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
# import jsonpickle

print(str(platform.platform()).split('-')[0])
if str(platform.platform()).split('-')[0] == 'macOS':
     Device.pin_factory = MockFactory() 

class Spe_sen_cdataset(): # data for speed sensor related calculation       
    def __init__(self):
        self.wheel_steps = 20 # num of holes in the disk 
        self.wheel_steps_counter = 0  # steps counter for steps required for a task 
        self.wheel_diameter = 6.6 
        self.wheel_circumference =  self.wheel_diameter * 3.14 # d x pi
        self.cms_per_step = self.wheel_circumference / self.wheel_steps  
        # self.speed = 0
        # self.interval = 10.0 # timer interval for calculatng RPM

class Pilot_d():
    def __init__(self) -> None:
        self.active = False
        self.cms = 0
        self.steps_rq = 0

class Kalyantra:
     
    def __init__(self):
        # Motor Driver Board L298N
        self.bot = Robot(left=(23,22),right=(18,17),pwm=False) 
        # Distance Sensor HC-SR04
        self.front_sensor = DistanceSensor(echo=6, trigger=5,threshold_distance=0.1)
        # IR Obstacle Sensor (Active Low)   
        self.back_sensor = DigitalInputDevice(pin=12)        
        # Speed Sensor LM393
        self.speed_sensor = DigitalInputDevice(pin=4)
        # Pi Camera (I'm using 5MP Pi Cam :( suggest to use high res cam :) )
        self.camera = PiCamera()  
        # TTS lib init (speakers connected to audio jack)
        # self.ttsen = pyttsx3.init()    

        # data
        self.move = 'halt' 
        self.moving = 'halt' 
            #"move" is setted as main movement after obstacle (halts) bot will resume to move in "move" direction
            #"moving" current status of bot moving for 
            #e.g if move is 'forward' 
            #moving=forward->obstacle->moving=halt->obstacle_cleared->moving=forward
        self.speed_sen_data = Spe_sen_cdataset()
        self.speed_cal_timer = ResetTimer(None,None)
        self.pilot_data = Pilot_d() # auto pilot mode to travel certain distance
        
    def speak(self,text):
        os.system(f"espeak -g 6 -s 210 '{text}'")
        
    #controls bot movement
    async def moves(self,move,main=False,cms=0) -> str:
        try:
            
            if main: self.move = move 
            self.moving = move 

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

            match(move):
                    
                case move_en.FORWARD.value: 
                    self.bot.forward()
                    self.speak("Moving forward")
                    return "done"              

                case move_en.BACKWARD.value:
                    self.bot.backward()
                    self.speak("Moving backward")
                    return "done" 
                     
                case move_en.RIGHT.value:
                    self.bot.right()
                    self.speak("Turning right")
                    return "done"

                case move_en.LEFT.value:
                    self.bot.left() 
                    self.speak("Turning left")
                    return "done"

                case move_en.HALT.value:
                    self.bot.stop() 
                    self.speak("Halt")
                    return "done"  
             
                    
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
                    if evnt == sensors_en.DEACTIVE and self.moving == 'forward':
                        # print("obstacle: stoping was moving forward")
                        asyncio.run(self.moves(move='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move == 'forward':
                        # print("clear: continue move forward")
                        asyncio.run(self.moves(move='forward'))
                        return

                case sensors_en.BACK:  
                    if evnt == sensors_en.DEACTIVE and self.moving == 'backward':
                        # print("obstacle: stoping was moving backward")
                        asyncio.run(self.moves(move='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move == 'backward':
                        # print("clear: continue move backward")
                        asyncio.run(self.moves(move='backward'))
                        return  

                case sensors_en.SPEED:
                    # keep steps counts by sensor event and handle pilot
                    # def count_wheel_steps(self):
                    self.speed_sen_data.wheel_steps_counter += 1
                    print(self.speed_sen_data.wheel_steps_counter)
                    if self.pilot_data.active :
                        if self.speed_sen_data.wheel_steps_counter > self.pilot_data.steps_rq :
                            print(f"pilot: done moving cms: {self.pilot_data.cms} steps: {self.pilot_data.steps_rq} ")
                            self.pilot_data.active = False
                            asyncio.run(self.moves(move='halt',main=True))
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
            
            # firebase
            blob = bucket.blob(file_name)
            blob.upload_from_filename(file_path) 
            return file_name
        
        except Exception as e:
            print(f"err at click_pic: {e}")  


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

kalyantra.front_sensor.when_in_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.DEACTIVE)
kalyantra.front_sensor.when_out_of_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.ACTIVE)

kalyantra.back_sensor.when_activated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.ACTIVE)
kalyantra.back_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.DEACTIVE)

kalyantra.speed_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.SPEED,event=sensors_en.DEACTIVE)


# kalyantra.speed_timer_do('set')
# kalyantra.speed_timer_do('run')
 
   