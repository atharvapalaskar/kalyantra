from flask import Blueprint
from bot_moves import show

base = Blueprint('base', __name__,)
moves = Blueprint('moves', __name__,url_prefix='/moves')
  
@base.get('/')
async def hello(): 
    return "ok",200

@moves.post('/<move>')
def mo(move):
    return show(move)

