from enum import Enum

class sub_topic_en(Enum):
    BASE = 'base'
    MOVE = 'move'   
    PICAM = 'picam'
    VCMD = 'vcmd'


class pub_topic_en(Enum):
    STATUS = 'status'
    TASK = 'task'
    SENSOR = 'sensor'  
    ACKS = 'acks'
    ERR = 'err'  

class move_en(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    RIGHT = 'right'
    LEFT = 'left'
    HALT = 'halt'

class sensors_en(Enum):
    FRONT = 'front'
    BACK = 'back'
    SPEED = 'speed'
    ACTIVE = 'active'
    DEACTIVE = 'deactive'
