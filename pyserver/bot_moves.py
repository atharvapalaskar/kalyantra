from flask import abort
 
def show(move):
    try:
        return f"done {move}",202
    except :
        abort(404)