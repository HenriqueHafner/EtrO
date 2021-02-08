import eel

class GUI():
    
    @eel.expose
    def UpdateClient():
        return ClientState
    
    def __init__(self):
        global ClientState
        ClientState = [1,3]
        return None
    
    def run(self):
        eel.init('web')
        print('EtrO App webserver starting..')
        eel.start('cncmachinedashboard.html',mode=False)
        return None