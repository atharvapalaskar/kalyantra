import json
import os 
import asyncio
from time import sleep
from datetime import datetime
from picamera import PiCamera   
from utils import bucket
from gpiozero import Device, DistanceSensor, DigitalInputDevice, RGBLED , Motor, Robot
from colorzero import Color 
import platform
from gpiozero.pins.mock import MockFactory
from timer_util import ResetTimer 
from enums import *  
import logging 
from datetime import datetime
import re
from utils import mq_client
import speech_recognition as sr  

logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO)

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
        # Turning
        self.turning = False  
        self.turn_steps = 0 
            # below values are to be predifined and might differ in each case
        self.turn_steps_req_right = 20 # approx 90 degrees 
        self.turn_steps_req_left = 20   
            # factors like body weight, wheel type and traction on diff surface will directly affect turn logic
            # for betterment use PWM motors instead of BO Motor with more calculative algorithm for precision
            # also better to keep a metal body(or any stable chassis) over fiber if using heaving comps

class KBot:
    def __init__(self):
        self.MotorsL = Motor(23,22,enable=24)
        self.MotorsR = Motor(18,17,enable=27)  
    
    def forward(self,speed):
        self.MotorsL.forward(speed)
        self.MotorsR.forward(speed)

    def backward(self,speed):
        self.MotorsL.backward(speed)
        self.MotorsR.backward(speed)
    
    def right(self,speed):
        self.MotorsR.stop()
        self.MotorsL.forward(speed)      
    
    def left(self,speed):
        self.MotorsL.stop() 
        self.MotorsR.forward(speed)       
    
    def halt(self):
        self.MotorsR.stop()
        self.MotorsL.stop()   


class Kalyantra:
     
    def __init__(self):
        # Motor Driver Board L298N
        # note on movement can be a personal choice from: 
           # 1. 'Robot' class from gpiozero -> Four wheel drive for turning (rotation) 
           # 2. KBot class -> Two wheel drive for turning (rotation)
        self.bot = Robot(left=(23,22,24),right=(18,17,27),pwm=True,) 
        self.bot = KBot() 
        # Distance Sensor HC-SR04
        self.distance_sensor = DistanceSensor(echo=6, trigger=5,threshold_distance=0.25)
        # IR Obstacle Sensor (Active Low)   
        self.front_sensor = DigitalInputDevice(pin=25)        
        # IR Obstacle Sensor (Active Low)   
        self.back_sensor = DigitalInputDevice(pin=12)        
        # Speed Sensor LM393 (IR Encoder Sensor)
        self.speed_sensor = DigitalInputDevice(pin=4)
        # Speed Sensor LM393 (IR Encoder Sensor)
        self.speed_sensor_r = DigitalInputDevice(pin=16)
        # After wake up waiting listening for tasks indicator LED
        self.led = RGBLED(26,20,21)
        # Pi Camera (I'm using 5MP Pi Cam :( suggested to use high res cam :) )
        self.camera = PiCamera() 
    
        self.srecg = sr.Recognizer() 
        self.mic = sr.Microphone()#device_index=1

        # data 
        self.awaiting_awake_cmd = True
        self.clicking_pic = False
        self.listening_wtd = False
        self.move = move_en.HALT.value
        self.moving = False
            # "move" is setted as main 'direction of movement'; after obstacle(halt) clearance -> bot will resume to move in "move" direction
            # "moving" current status of bot moving for  
            # Flow: moving=True -> obstacle->moving=False -> obstacle_cleared->moving=True
        self.frontClear = True
        self.backClear = True
        self.speed_sen_data = Spe_sen_cdataset()
        # self.speed_cal_timer = ResetTimer(None,None)
        self.pilot_data = Pilot_d() # auto pilot mode to travel certain distance
        self.total_steps = 0 #lifetime travel
        self.steps_away_from_orgin = 0 #current away from origin
        self.moves_away_from_origin = [] 
        self.task_name = 'any'
        self.current_task = '--'
        self.last_task = '--' 
        self.next_task = '--'
        self.to_do_tasks = []
        self.temp_return_tasks = []
        # 
        self.tracing_path = False 
         
    def speak(self,text): 
        print("speakingg ")
        os.system(f"espeak -g 6 -s 210 '{text}'") 
        
    #controls bot movement
    async def moves(self,msg:str=None,main=False,resume=False) -> str:
        try:
            
            if msg == None and not resume: return
           
            if not resume:
                cms = 0  
                move = msg.split(' ')[1 if msg.startswith('move') else 0].strip() 
                val = int(re.findall(r'\d+', msg)[0]) if len(re.findall(r'\d+', msg)) > 0 else 0
                if msg.endswith(' m'):val = val * 100  #convert m to cm 
                cms = val
                print(f'move msg: {cms} cm')  

                mvs = [mv.value for mv in move_en]
                if mvs.count(move) < 1 : return

                if main: 
                    self.move = move 
                    self.tasks_update(task= msg if msg.startswith('move') else f'move {msg}') 
                  #to-do ===>
                    # if self.move != move_en.HALT.value : self.moves_away_from_origin.append(msg.split('move')[1].strip() if msg.startswith('move') else msg)
                    # print(f'moves aways = {self.moves_away_from_origin}')
                  #<===

                self.moving = True if move != move_en.HALT.value else False 

                if cms != 0: 
                    self.speed_sen_data.wheel_steps_counter = 0     
                    # convert cm to steps : num of steps required to travel a distance in centimeters
                    steps_req = cms / self.speed_sen_data.cms_per_step 
                    self.pilot_data.steps_rq = steps_req
                    self.pilot_data.cms = cms
                    self.pilot_data.active = True 
            
            else:
                # resume after halt interrupt eg from mic
                print('resume')
                move = self.move
                self.moving = True if move != move_en.HALT.value else False 
                    # was turning 
                if move == move_en.RIGHT or move == move_en.LEFT.value and not self.pilot_data.turning :
                   move = move_en.FORWARD.value
                print(f'resume move = {move}, ac mv: {self.move}, wasTurnn: {self.pilot_data.turning} ')
            
            self.led_handler()
            # speakStr = ''
            match(move):
              
                case move_en.FORWARD.value: 
                    self.bot.forward(0.25) 
                    # speakStr = "Moving forward" 

                case move_en.BACKWARD.value:
                    self.bot.backward(0.25)
                    # speakStr = "Moving backward" 
                     
                case move_en.RIGHT.value: 
                    self.pilot_data.turning = True
                    self.bot.right(0.5)  
                    # speakStr = "Turning right" 

                case move_en.LEFT.value:
                    self.pilot_data.turning = True
                    self.bot.left(0.5) 
                    # speakStr = "Turning left" 

                case move_en.HALT.value:
                    self.bot.halt() 
                    # speakStr = "Halt"  

                case move_en.UTURN.value:
                    self.pilot_data.turning = True
                    self.bot.right(0.5) 
                    # speakStr = "Halt"  

                case _:
                    raise Exception('Unkown move') 
                 
            mq_client.publish(pub_topic_en.TASK.value,
               payload=json.dumps({"data":{"taskName":self.task_name,"currentTask":self.current_task,"nextTask":self.next_task,"lastTask":self.last_task,"move":self.move,"moving":self.moving,"pilot":self.pilot_data.active}}),
               qos=1) 
            # self.speak(speakStr) 
                   
        except Exception as e: 
            return f"error at moves({move,main}) : {e}" 

        
    # sensor events callback to control movement
    def sensors_n_moves(self,*args,**kwargs): 
        senr = kwargs['sensor'] 
        evnt = kwargs['event'] 
        rt = kwargs['rt']  
        # print(f"sensor:{senr}, event:{evnt}") 
                        
        try:
            match(senr):
                    
                case sensors_en.FRONT:  
                    if evnt == sensors_en.DEACTIVE and self.move != 'halt' and self.move != 'backward' and self.moving :
                        self.frontClear = False
                        # print("obstacle: stoping was moving forward") 
                        mq_client.publish(pub_topic_en.SENSOR.value,payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear,}}),qos=1) 
                        asyncio.run(self.moves(msg='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move != 'halt' and self.move != 'backward':
                        self.frontClear = True
                        # print("clear: continue move forward")
                        mq_client.publish(pub_topic_en.SENSOR.value,payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear}}),qos=1) 
                        asyncio.run(self.moves(msg='forward'))
                        return

                case sensors_en.BACK:   
                    if evnt == sensors_en.DEACTIVE and self.move != 'halt' and self.move != 'forward' and self.moving :
                        self.backClear = False
                        # print("back_obstacle: stoping was moving backward")
                        mq_client.publish(pub_topic_en.SENSOR.value,payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear,}}),qos=1) 
                        asyncio.run(self.moves(msg='halt'))
                        return
                    elif evnt == sensors_en.ACTIVE and self.move != 'halt' and self.move != 'forward' :
                        self.backClear = True
                        # print("back_clear: continue move backward")
                        mq_client.publish(pub_topic_en.SENSOR.value,payload=json.dumps({"data":{"frontClear":self.frontClear,"backClear":self.backClear}}),qos=1) 
                        asyncio.run(self.moves(msg='backward'))
                        return  
               
                # keep steps counts by sensor event and handle pilot 
                case sensors_en.SPEED:
                    # ignore left sens if move left
                    if not rt and self.move == move_en.LEFT.value: return
                    # ignore right sens events as move not left
                    if rt and self.move != move_en.LEFT.value: return
                    # handle turning 
                        # eg if move left: then only take a LEFT TURN  
                        # elif move left 'n' cm: then take a LEFT TURN and MOVE FORWARD 'n' cm
                    if self.pilot_data.turning: 
                       self.pilot_data.turn_steps += 1 
                       strq = self.pilot_data.turn_steps_req_right if self.move == move_en.RIGHT.value else self.pilot_data.turn_steps_req_right * 2 if  self.move == move_en.UTURN.value else self.pilot_data.turn_steps_req_left
                       if self.pilot_data.turn_steps > strq:
                            print(f"{self.move}: done turning : {strq} steps: {self.pilot_data.turn_steps} ")
                            asyncio.run(self.moves(msg='halt')) 
                            self.pilot_data.turning = False 
                            self.pilot_data.turn_steps = 0
                            # cms was given move forward
                            if self.pilot_data.cms != 0 :
                               sleep(0.5)
                               asyncio.run(self.moves(msg=f'forward {self.pilot_data.cms} cm'))
                            else:
                               asyncio.run(self.moves(msg='halt',main=True))
                            return
                    # handle steps and pilot
                    else:
                        if self.moving : 
                            self.speed_sen_data.wheel_steps_counter += 1 
                            self.total_steps += 1
                            print(self.speed_sen_data.wheel_steps_counter)
                        if self.pilot_data.active :
                            if self.speed_sen_data.wheel_steps_counter > self.pilot_data.steps_rq :
                                asyncio.run(self.moves(msg='halt')) 
                                self.tasks_next_handler() 
                        
        except Exception as e:
            print(f"err at sensors_n_moves({senr},{evnt}): {e}") 


    #click photo and upload to firebase
    async def click_pic(self,msg=None):         
        try:
            if self.moving or msg == None: 
                mq_client.publish(pub_topic_en.ACKS.value,payload='caut:busy',qos=1)   
                return None
            
            m = str(msg.split(' ')[0]).strip()
            match (m): 
                case 'click':
                   
                    self.tasks_update(task='click a photo') 
                    self.clicking_pic = True
                    self.led_handler()
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

                    mq_client.publish(pub_topic_en.ACKS.value,payload=f"uploaded: {file_name}",qos=1)   
                    self.clicking_pic = False
                    self.led_handler()
                    return file_name
                
                case _: 
                    self.clicking_pic = False
                    self.led_handler()
                    print('unhandled camera event')
        
        except Exception as e:
            logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} err at click_pic(): {e}") 

  
    def tasks_creator(self,msg): #vcmd entry point  
        dotxt = msg.lower()
        self.task_name = dotxt 

        # many tasks : 
          # eg move forward 30 cm then click a photo move left 10 cm then click a photo and move backward 10 cm
        if dotxt.count('then') > 0: 
            and_split = dotxt.split('and')
            tasks = and_split[0].split('then')
            tasks.append(and_split[1])  
        # two tasks: eg move forward 10 cm and click a photo
        elif dotxt.count('and') > 0: tasks = dotxt.split('and')
        # single task: eg move right 15 cm
        else: tasks = [dotxt] 
          
        self.to_do_tasks = [task.strip() for task in tasks] 
         
        if self.to_do_tasks[0].startswith('click'):
            kalyantra.speak('Task Accepted')
            sleep(0.4)
            asyncio.run(self.click_pic(msg='click'))  
            self.tasks_next_handler() 
            
        elif self.to_do_tasks[0].startswith('move'): 
            kalyantra.speak('Task Accepted')
            sleep(0.4)
            self.pilot_data.active = True
            asyncio.run(self.moves(msg=msg,main=True))
            return 
        
    #to-do ===>
        # elif self.to_do_tasks[0].startswith('go to'):
        #     # eg go to kitchen 
        #     kalyantra.speak('Task Accepted')
        #     sleep(0.4)
        #     self.pilot_data.active = True
        #     asyncio.run(self.moves(msg=msg,main=True))
        #     return   
    # <===

        elif self.to_do_tasks[0].startswith('return'): 
            kalyantra.speak('Task Accepted')
            sleep(0.4)
            self.pilot_data.active = True
            asyncio.run(self.moves(msg=msg,main=True))
            return 
        
        else : 
            self.to_do_tasks = [0]
            kalyantra.speak('Bad Tasks')
            # raise Exception('bad pilot tasks')
    
    #to-do ===>
        # after all tasks return; from where the current todo first task started  
        # eg already away from origin (assume origin pt. A0 and currently at pt. D20 by moves[x directions and n distance] )
           # from D20 -> (vcmd: move forwad 30 cm then move right 2m and return )
           # after right 2m -> will return to D20
           
        # if str(self.to_do_tasks[len(self.to_do_tasks)-1]).startswith('return'):
        #     self.to_do_tasks.pop()  
        #     self.create_return_tasks(to_origin=false)
    # <===
    

    def tasks_update(self,task=None):
        # from loop of multiple tasks    
        if self.pilot_data.active and len(self.to_do_tasks) > 0: 
            self.last_task = self.current_task
            self.current_task = self.to_do_tasks[0]
            self.next_task = self.to_do_tasks[1] if len(self.to_do_tasks) > 1 else '--' 
            # print('update tasks with next')
            mq_client.publish(pub_topic_en.TASK.value,
                payload=json.dumps({"data":{"taskName":self.task_name,"currentTask":self.current_task,"nextTask":self.next_task,"lastTask":self.last_task,"move":self.move,"moving":self.moving,"pilot":self.pilot_data.active}}),
                qos=1) 
            return  
        # single task
        elif task != None:
            self.last_task = self.current_task
            self.current_task = task
            self.next_task = '--'   
            mq_client.publish(pub_topic_en.TASK.value,
                payload=json.dumps({"data":{"taskName":self.task_name,"currentTask":self.current_task,"nextTask":self.next_task,"lastTask":self.last_task,"move":self.move,"moving":self.moving,"pilot":self.pilot_data.active}}),
                qos=1) 
            return
        else : raise Exception('bad task updation')   

           
    def tasks_next_handler(self):
        try:
            # remove current task
            if len(self.to_do_tasks) > 0: 
                self.to_do_tasks.pop(0)
            # next task
            if self.next_task != '--':              
                if self.next_task.startswith('click'):
                    asyncio.run(self.click_pic(msg='click'))  
                    self.tasks_next_handler() 
                else: 
                    sleep(0.5)  
                    asyncio.run(self.moves(msg=self.next_task,main=True)) 
                    return
            # no next task
            else :
                self.pilot_data.active = False 
                self.pilot_data.cms = 0
                asyncio.run(self.moves(msg='halt',main=True))
                return
        
        except Exception as e:
            print(f'err at tasks_next_handler() :{e}')
 
 
   #(not fully tested feature and to-do)===>
    def create_return_tasks(self): 
       
        temp_return_tasks = []
 
        rma = self.moves_away_from_origin
        rma.reverse() 

        fval = int(re.findall(r'\d+',self.rma[0])[0])
        print(fval)
        temp_return_tasks.append('uturn')
        temp_return_tasks.append(f"forward {fval} cm") 
        route_cms = [int(re.findall(r'\d+', move_cm)[0]) for move_cm in rma] 
        route_cms.pop(0)
        print(route_cms)

        for i in range(len(route_cms)): 
            mvk = rma[i]
            print(mvk)
            if str(mvk).startswith(move_en.FORWARD.value):
                # mv = ''.join([move_en.BACKWARD.value,str(mvk).split(move_en.FORWARD.value)[1]]).strip() 
                print('')
            elif str(mvk).startswith(move_en.BACKWARD.value): 
                # mv = ''.join([move_en.FORWARD.value,str(mvk).split(move_en.BACKWARD.value)[1]]).strip()
                print('')
            elif str(mvk).startswith(move_en.RIGHT.value): 
                mv = ' '.join([move_en.LEFT.value,str(route_cms[i]),str(mvk).split(' ')[2]]).strip() 
            elif str(mvk).startswith(move_en.LEFT.value): 
                mv = ' '.join([move_en.RIGHT.value,str(route_cms[i]),str(mvk).split(' ')[2]]).strip() 
            else: raise Exception('cant create return task')

            temp_return_tasks.append(mv) 

        print(self.temp_return_tasks)
    # <===

    def led_handler(self): 
         self.led.off()
         if self.listening_wtd: 
            self.led.color = Color('purple')
         elif self.clicking_pic:
            self.led.color = Color('limegreen')
         elif self.moving == False and self.move != move_en.HALT.value:
            self.led.color = Color('red')
         elif self.pilot_data.active:
            self.led.color = Color('orange')
         elif self.tracing_path:
            self.led.color = Color('lightblue')
         else : 
            self.led.color = Color('green') if self.awaiting_awake_cmd else  Color('white')
            # self.led.pulse(fade_in_time=1, fade_out_time=3, on_color=(0, 1, 0), off_color=(1, 1, 1), n=None, background=True)

    # unused
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
    # kalyantra.distance_sensor.when_in_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.DISTANCE,event=sensors_en.DEACTIVE)
    # kalyantra.distance_sensor.when_out_of_range =  lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.DISTANCE,event=sensors_en.ACTIVE)

    kalyantra.front_sensor.when_activated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.ACTIVE,rt=None)
    kalyantra.front_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.FRONT,event=sensors_en.DEACTIVE,rt=None)

    kalyantra.back_sensor.when_activated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.ACTIVE,rt=None)
    kalyantra.back_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.BACK,event=sensors_en.DEACTIVE,rt=None)

    kalyantra.speed_sensor.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.SPEED,event=sensors_en.DEACTIVE,rt=False)
    kalyantra.speed_sensor_r.when_deactivated = lambda s: kalyantra.sensors_n_moves(s,sensor=sensors_en.SPEED,event=sensors_en.DEACTIVE,rt=True)

 
# kalyantra.speed_timer_do('set')
# kalyantra.speed_timer_do('run')
 