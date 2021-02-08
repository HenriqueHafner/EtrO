# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import serial
import serial.tools.list_ports as lp #return a object list with serial ports information

class SerialCNCInterface():
    def __init__(self):
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA' #Arduino Clone Instance, reference hwid
        self.SerialPorts = lp.comports()
        for i in self.SerialPorts:
            if i.hwid == self.Controller_hwid:
                self.ControllerPortName = i.name
                print('Found Serial port for Controler with ',self.Controller_hwid,' hwid')
            else:
                self.ControllerPortName = False
        self.ControllerCOM = object #this object will be further overwrited by the serial comunmicator instance
        

    def bind_communication(self,ControllerPortName):
        if ControllerPortName != False:
            self.ControllerCOM = serial.Serial(port=ControllerPortName,baudrate=250000,timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
        return True

    def readCNCserial(self,char_limit=1024,stability_sleep=True,decodemode='utf-8'):
        if stability_sleep==True:
            time.sleep(0.2)
        message = self.ControllerCOM.read(char_limit)
        message = message.decode(decodemode)
        return message

    def CNCStatus(self):
        status = []
        self.ControllerCOM.flush()
        self.ControllerCOM.write(bytes("M105\n","utf-8"))
        status.append(self.readCNCserial())
        return status

    def close(self):
        self.ControllerCOM.close()
        return True

    def run(self):
        self.bind_communication(ControllerPortName=self.ControllerPortName)


# CncInterface = SerialCNCInterface()
# CncInterface.run()



