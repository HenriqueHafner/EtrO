# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import serial
import serial.tools.list_ports as lp #return a object list with serial ports information
import glob
import os

class serial_cnc_interface():

    def __init__(self):
        #serial communication attributes
        self.setup_done = False
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA' #Arduino Clone Instance, reference hwid
        self.ControllerCOM = False #var will be further overwrited with serial comunmicator instance
        self.ControllerPortName = str #var with the part name 
        
        
        #comand_file attributes
        self.gcode_status = 0
        self.gcode_custom_message = ['Null']
        self.gcode_data = [['0'],5,'Null',0] # [Gcode File, file line pos,file name, end of file line index]
        self.gcode_datas_dir = ['']
        self.gcode_data_name = 'Null'
        self.gcode_data_adress = 'Null'
        self.gcode_datas_list = ['Null']
        self.gcode_custom_message = []

    def find_serial_device(self):
        self.SerialPorts = lp.comports()
        for i in self.SerialPorts:
            if i.hwid == self.Controller_hwid:
                self.ControllerPortName = i.name
                print('Found Serial port for Controler with ',self.Controller_hwid,' hwid')
                return True
        self.ControllerPortName = 'Null'
        return False
        
    def bind_communication(self):
        ControllerPortName = self.ControllerPortName
        if ControllerPortName != 'Null':
            self.ControllerCOM = serial.Serial(port=ControllerPortName,baudrate=250000,timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
            return True
        else:
            return False

    def read_cnc_serial(self,stability_sleep=True,char_limit=1024,feedback=False,feedback_timeout=20,debug=True):
        #check if binded
        if self.ControllerCOM == False:                
            print('No serial device binded.')
            return False
        
        # feedback waiting block
        if feedback != False:  
            rear = True
            stime = time.time()
            while rear == True:
                message = self.ControllerCOM.read(len(feedback))
                if debug == True: print(message)
                if message == feedback:
                    rear = False
                    return 'FB1'
                elif len(message) > 0:
                    print(message)
                    rear = False
                    return 'recieved feedback message is not the expected flag.'
                elif time.time()-stime > feedback_timeout:
                    rear = False
                    return 'Timeout, '+str(feedback_timeout)+' seconds with no respose.'
                time.sleep(0.02)
        
        #Simple read block
        if stability_sleep==True:
            time.sleep(0.1)
        message = self.ControllerCOM.read(char_limit)
        message = message.decode('utf-8')
        return message
    
    def write_cnc_serial(self,data,assure_ln=True):
        if self.ControllerCOM == False:
            print('Missing serial Device. ',data)
            return False            
        if assure_ln == True:          
            if data[-1] != '\n':
                data = data+'\n'
        data = bytes(data,'utf-8')
        self.ControllerCOM.write(data)
        feedback_answer = self.read_cnc_serial(feedback=bytes('ok\n','utf-8'),char_limit=3)
        if feedback_answer == 'FB1':
            return 'FB1'
        elif feedback_answer == True:
            return True
        else:
            print(feedback_answer)
            return False

    def CNCStatus(self):
        status = 'Null'
        try:
            self.ControllerCOM.flush()
            self.ControllerCOM.write(bytes("M105\n","utf-8"))
            status=self.read_cnc_serial()
        except:
            status = 'Failed to comunicate.'
        return status

    def close(self):
        self.ControllerCOM.close()
        return True

    def gcode_set_data(self):
        with open(self.gcode_data_adress) as f:
            gcode_data_l = f.read()
        gcode_data_l = gcode_data_l.split('\n')
        target_file_index = self.gcode_data_adress.rindex('\\') #finding star position of file name string.
        gcode_data_name_l = self.gcode_data_adress[target_file_index+1:] #extracting the file_name from path
        self.gcode_data_name = gcode_data_name_l
        self.gcode_data[0] = gcode_data_l
        self.gcode_data[1] = 0
        self.gcode_data[2] = gcode_data_name_l
        self.gcode_data[3] = len(gcode_data_l)-1 # subtractin 1 to start in line 0 index 0
        return True

    def gcode_data_handler(self,arg_def='test',gcode_datas_dir_l='None'):#pick a gcode file
        if gcode_datas_dir_l == 'None':
            gcode_datas_dir_l = os.getcwd()

        if arg_def == 'test':
            gcode_data_name_l = 'test.gcode' # _l means a local scope var of instance propertie.
            gcode_datas_list_l = glob.glob(os.path.join(gcode_datas_dir_l,'*.gcode'))
        elif arg_def == 'GetNewest':
            gcode_datas_list_l = glob.glob(os.path.join(gcode_datas_dir_l,'*.gcode'))
            gcode_datas_list_l.sort(key=os.path.getctime,reverse=True)
            target_file_index = gcode_datas_list_l[0].rindex('\\') #finding star position of file name string.
            gcode_data_name_l = gcode_datas_list_l[0][target_file_index+1:] #extracting the file_name from path
        elif type(arg_def) == list: #set a path in index 0 and file name in index 1
            gcode_data_name_l = arg_def[1]
            gcode_datas_dir_l = arg_def[0]           
            gcode_datas_list_l=[os.path.join(gcode_datas_dir_l,gcode_data_name_l)]
        else:
            print('Unexpected arg_def argument.')
            return False
        
        self.gcode_data_name = gcode_data_name_l
        self.gcode_datas_dir = gcode_datas_dir_l
        self.gcode_datas_list = gcode_datas_list_l
        self.gcode_data_adress = os.path.join(gcode_datas_dir_l,gcode_data_name_l)
        return True

    def gcode_stream_handler(self): #flush not working!!!
        if self.gcode_custom_message != ['Null']:
            self.ControllerCOM.flush()
            for custom_message in self.gcode_custom_message:
                self.write_cnc_serial(custom_message)
            #self.gcode_custom_message = ['Null']
        if self.gcode_status == 0:
            return 'gcode_handler Idle'
        elif self.gcode_status == 1:
            return self.stream_gcode()

    def stream_gcode(self):
        gc_line_pos = self.gcode_data[1]
        gc_linebwrite = self.gcode_data[0][gc_line_pos]
        self.gcode_data[1] +=1
        if gc_linebwrite[0] == ';':
            return 'Not valid command line'
        self.write_cnc_serial(gc_linebwrite)
        return True 
    
    def gcode_move_lastlinepos(self,line,operator='abs'):
        curr_line = self.gcode_data[1]
        target_line = None
        if operator == 'abs':
            target_line = line
        elif operator == 'relative':
            target_line = curr_line+line
        if target_line < 0:
            print('requested target_line was negative. Going to 0 instead')
            target_line = max(0,target_line)
        self.gcode_data[1] = target_line
        return True
        
    def gcode_command_inster(command='None'):
        return

    def run(self):
        self.find_serial_device()
        self.bind_communication()
        self.gcode_data_handler('GetNewest')
        self.gcode_set_data()
        self.setup_done = True


#quando recarregado, file_handler nao atualiza as propriedades gcode_data
test = False
if test == True:
   tester = serial_cnc_interface()
   tester.gcode_custom_message = ['G1 F480 X101.084 Y92.419','G1 X101.379 Y92.547','G1 X103.682 Y92.844','G1 X104.345 Y92.969','G1 X104.989 Y93.173','G1 X105.604 Y93.45','G1 X106.182 Y93.799','G1 X106.557 Y94.08','G1 X107.164 Y94.287','G1 X107.958 Y94.685','G1 X109.303 Y95.497','G1 X109.387 Y95.524','G1 X110 Y95.805','G1 X110.576 Y96.157','G1 X111.011 Y96.5','G1 F480 X101.084 Y92.419','G1 X101.379 Y92.547','G1 X103.682 Y92.844','G1 X104.345 Y92.969','G1 X104.989 Y93.173','G1 X105.604 Y93.45','G1 X106.182 Y93.799','G1 X106.557 Y94.08','G1 X107.164 Y94.287']
   tester.run()
   #tester.write_cnc_serial('G28 X Y')
   #tester.gcode_stream_handler()
    









