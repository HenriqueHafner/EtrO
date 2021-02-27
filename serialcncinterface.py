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

class SerialCNCInterface():

    def __init__(self):

        #serial communication attributes
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA' #Arduino Clone Instance, reference hwid
        self.SerialPorts = lp.comports()
        self.ControllerCOM = False #this object will be further overwrited by the serial comunmicator instance
        for i in self.SerialPorts:
            if i.hwid == self.Controller_hwid:
                self.ControllerPortName = i.name
                print('Found Serial port for Controler with ',self.Controller_hwid,' hwid')
            else:
                self.ControllerPortName = False

        #comand_file attributes
        self.gcode_status = 0
        self.gcode_custom_message = ['Null']
        self.gcode_file = [[0],5,'Null',0] # [Gcode File, file line pos,file name,file lines size]
        self.gcode_files_dir = ['']
        self.gcode_file_adress = os.path.join(os.getcwd(),'test.gcode')
        self.gcode_files_list = [self.gcode_file_adress]

            
    def bind_communication(self,ControllerPortName):
        if ControllerPortName != False:
            self.ControllerCOM = serial.Serial(port=ControllerPortName,baudrate=250000,timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
            return True
        else:
            return False

    def read_cnc_serial(self,stability_sleep=True,char_limit=1024,decodemode='utf-8',feedback=False,feedback_timeout=20):
        # feedback waiting block
        if feedback != False:
            rear = True
            stime = time.time()
            while rear == True:
                message = self.ControllerCOM.read(char_limit)
                if message == feedback:
                    rear = False
                    return True
                elif len(message) > 0:
                    rear = False
                    return 'recieved feedback message is unexpected.'
                elif time.time()-stime > feedback_timeout:
                    rear = False
                    return 'Timeout, '+str(feedback_timeout)+' seconds with no respose.'
                time.sleep(0.02)
        
        #Simple read block
        if stability_sleep==True:
            time.sleep(0.1)
        message = self.ControllerCOM.read(char_limit)
        message = message.decode(decodemode)
        return message
    
    def write_cnc_serial(self,data):
        if self.ControllerCOM != False:
            self.ControllerCOM.write(data)
            feedback_answer = self.read_cnc_serial(feedback='ok!'.encode('utf-8'))
            if feedback_answer != True:
                print(feedback_answer)
            return True
        else:
            print('Missing serial Device. ',data)
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

    def get_gcode_data(self,fileadress):       
        with open(fileadress) as f:
            gcode_data = f.read()
        gcode_data = gcode_data.split('\n')
        return gcode_data

    def stream_gcode(self):
        gc_line_pos = self.gcode_file[1]
        gc_linebwrite = self.gcode_file[0][gc_line_pos]
        self.gcode_file[1] +=1
        if gc_linebwrite[0] == ';':
            return 'Not valid command line'
        gc_linebwrite = gc_linebwrite.encode('utf-8')
        self.write_cnc_serial(gc_linebwrite)
        return True 
    
    def gcode_move_lastlinepos(self,line,operator='abs'):
        curr_line = self.gcode_file[1]
        target_line = None
        if operator == 'abs':
            target_line = line
        elif operator == 'relative':
            target_line = curr_line+line
        if target_line < 0:
            print('requested target_line was negative. Going to 0 instead')
            target_line = max(0,target_line)
        self.gcode_file[1] = target_line
        return True
        
    def gcode_file_handler(self,arg_def='test'):#fazer o ponteiro andar sobre os códigos
        if arg_def == 'test':
            self.gcode_files_dir = os.getcwd()
            filename='test.gcode'
        elif arg_def == 'GetNext' or arg_def == 'GetPrev':
            self.gcode_files_list = glob.glob(os.path.join(self.gcode_files_dir,'*.gcode'))
            self.gcode_files_list.sort(key=os.path.getctime,reverse=True)
        elif type(arg_def) == list:
            self.gcode_files_dir = arg_def[0]           
            filename = arg_def[1]
        else:
            return False
        self.gcode_file_adress = os.path.join(self.gcode_files_dir,filename)
        return True

    def gcode_stream_handler(self):
        if self.gcode_custom_message != ['Null']:
            for custom_message in self.gcode_custom_message:
                b_custom_message = custom_message.encode('utf-8')
                self.write_cnc_serial(b_custom_message)
            self.gcode_custom_message = ['Null']
        if self.gcode_status == 0:
            return 'gcode_handler Idle'
        elif self.gcode_status == 1:
            return self.stream_gcode()

        
    
    def run(self):
        #self.bind_communication(ControllerPortName=self.ControllerPortName)
        self.gcode_file[0] = self.get_gcode_data(self.gcode_file_adress)


    









