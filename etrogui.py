import eel
  
class gui():
    
    def __init__(self):
        self.machine_interface_obj = None
        self.gdws = 11 
        self.gcode_display = ['-']*self.gdws     
    
    def run_webserver(self):
        eel.init('web')
        print('EtrO App webserver starting..')
        eel.start('cncmachinedashboard.html',port=80)
        print('EtrO App webserver Closed..')
        return None
    
    def set_machine_interface(self,mi_instance):
        self.machine_interface_obj = mi_instance
    
    def update_terminal_gcode(self): #gdws is gcode_display_window_size , need to be odd number
        gdwi = [self.machine_interface_obj.gcode_data[1]]*self.gdws #gcode_display_window_index
        display_gcode_shift = [] #gcode index shifter to display window
        for i in range(self.gdws):
            display_gcode_shift.append(int(i-((self.gdws/2)-0.5))) #computing index
        for i in range(self.gdws):
            element_index = gdwi[i]+display_gcode_shift[i]
            if element_index >= 0 \
            and element_index < self.machine_interface_obj.gcode_data[3]:
                self.gcode_display[i] = str(element_index) + \
                ' : ' + self.machine_interface_obj.gcode_data[0][element_index]
            else:
                self.gcode_display[i] = ''
        return self.gcode_display
    
    def call_terminal_gcode(self,call_message):
        data = self.machine_interface_obj.terminal_gcode_caller(call_message)
        return data
    
    def update_monitor_serial(self):
        return self.machine_interface_obj.monitor_serial_update()
    
    def update_monitor_machine(self):
        return self.machine_interface_obj.monitor_machine_update()
    