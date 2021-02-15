import eel

global ClientState

# @staticmethod
# @eel.expose
# def UpdateClient():
#     global ClientState
#     return ClientState

class GUI():
    
    # @eel.expose
    # def UpdateClient():
    #     return ClientState
    
    def __init__(self):
#         global ClientState
#         self.ClientState = ['No data added']'
        return None

    def run_webserver(self):
        eel.init('web')
        print('EtrO App webserver starting..')
        eel.start('cncmachinedashboard.html',mode=False)
        return None
    
    #adicionar numero linha no plot, remover .gcode_file da funcao, ssubstituir pelo valor como argumento
    def gcode_displaydata_fill(self,CncInterface,gdws=11): #gdws is gcode_display_window_size , need to be odd number
        self.gcode_display = ['-']*gdws 
        gdwi = [CncInterface.gcode_file[1]]*gdws #gcode_display_window_index
        display_gcode_shift = [] #gcode index shifter to display window
        for i in range(gdws):
            display_gcode_shift.append(int(i-((gdws/2)-0.5))) #computing index
        for i in range(gdws):
            element_index = gdwi[i]+display_gcode_shift[i]
            if element_index >= 0:
                self.gcode_display[i] = CncInterface.gcode_file[0][element_index]
            else:
                self.gcode_display[i] = ' '
        return True
    