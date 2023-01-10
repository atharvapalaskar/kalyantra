from enum import Enum

class topic_en(Enum):
    BASE = 'base'
    MOVE = 'move'   
    PICAM = 'picam'

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
