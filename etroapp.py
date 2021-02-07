import eel
import time

class etroapp():
    
    @eel.expose
    def UpdateClient():
        return ClientState
    
    def __init__(self):
        global ClientState
        ClientState = [1,3]
        print('EtrO App webserver starting..')
        eel.init('web')
        eel.start('main.html',mode=False)
        return None