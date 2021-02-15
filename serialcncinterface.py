# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import serial
import serial.tools.list_ports as lp #return a object list with serial ports information
import os

class SerialCNCInterface():

    def __init__(self):
        self.gcode_status = 0
        self.gcode_file = [[0],0,'Null',0] # [Gcode File, file line pos,file name,file lines size]
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA' #Arduino Clone Instance, reference hwid
        self.SerialPorts = lp.comports()
        self.ControllerCOM = object #this object will be further overwrited by the serial comunmicator instance

        for i in self.SerialPorts:
            if i.hwid == self.Controller_hwid:
                self.ControllerPortName = i.name
                print('Found Serial port for Controler with ',self.Controller_hwid,' hwid')
            else:
                self.ControllerPortName = False
            
    def bind_communication(self,ControllerPortName):
        if ControllerPortName != False:
            self.ControllerCOM = serial.Serial(port=ControllerPortName,baudrate=250000,timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
            return True
        else:
            return False

    def readCNCserial(self,char_limit=1024,stability_sleep=True,decodemode='utf-8'):
        if stability_sleep==True:
            time.sleep(0.2)
        message = self.ControllerCOM.read(char_limit)
        message = message.decode(decodemode)
        return message
    
    def write_cnc_serial(self,data):
        self.ControllerCOM.write(data)
        return

    def CNCStatus(self):
        status = 'Null'
        try:
            self.ControllerCOM.flush()
            self.ControllerCOM.write(bytes("M105\n","utf-8"))
            status=self.readCNCserial()
        except:
            status = 'Failed to comunicate.'
        return status

    def close(self):
        self.ControllerCOM.close()
        return True

    def get_gcode_data(self,file_adress):
        with open(file_adress) as f:
            gcode_data = f.read()
        gcode_data = gcode_data.split('\n')
        return gcode_data

    def stream_gcode(self):
        gc_line_pos = self.gcode_file[1]
        gc_linebwrite = self.gcode_file[0][gc_line_pos]
        self.gcode_file[1] +=1
        if gc_linebwrite[0] == ';':
            return None
        gc_linebwrite = gc_linebwrite.encode('utf-8')
        return gc_linebwrite 
    
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
                
    def gcode_handler(self):
        if self.gcode_status == 0:
            return 'gcode_handler Idle'
        elif self.gcode_status == 1:
            return self.stream_gcode()
    
    def run(self):
        self.bind_communication(ControllerPortName=self.ControllerPortName)
        self.gcode_file[0] = self.get_gcode_data(file_adress=os.path.join(os.getcwd(),'test.gcode'))


    









