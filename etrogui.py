import eel

global ClientState

# @staticmethod
# @eel.expose
# def UpdateClient():
#     global ClientState
#     return ClientState

class gui():
    
    def run_webserver(self):
        eel.init('web')
        print('EtrO App webserver starting..')
        eel.start('cncmachinedashboard.html',port=80)
        print('EtrO App webserver Closed..')
        return None
    
    def gcode_terminal_handler(self,cnc_interface_obj,): #gdws is gcode_display_window_size , need to be odd number
        gdws=11    
        self.gcode_display = ['-']*gdws 
        gdwi = [cnc_interface_obj.gcode_data[1]]*gdws #gcode_display_window_index
        display_gcode_shift = [] #gcode index shifter to display window
        for i in range(gdws):
            display_gcode_shift.append(int(i-((gdws/2)-0.5))) #computing index
        for i in range(gdws):
            element_index = gdwi[i]+display_gcode_shift[i]
            if element_index >= 0 \
            and element_index < cnc_interface_obj.gcode_max_index_line:
                self.gcode_display[i] = str(element_index) + \
                ' : ' + cnc_interface_obj.gcode_data[0][element_index]
            else:
                self.gcode_display[i] = ' '
        return self.gcode_display
    
    def monitor_serial_handler(self,cnc_interface_obj):
        return cnc_interface_obj.monitor_serial_update()
    
    def monitor_cnc_handler(self,cnc_interface_obj):
        return cnc_interface_obj.monitor_cnc_update()
    