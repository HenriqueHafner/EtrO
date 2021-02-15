# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:22:13 2020

@author: Henrique
"""

import threading
import time

import etrogui
import ControlerXbox
import serialcncinterface

GUI = etrogui.GUI()
CncInterface = serialcncinterface.SerialCNCInterface()

def ControlEvent(State,LastState):
    CliState=etrogui.ClientState[1]
    if LastState[1][4]-State[1][4] == 1: #(LB) was Released
        CliState -= 1
        print('(LB) was Released')
    if LastState[1][5]-State[1][5] == 1: #(RB) was Released
        CliState += 1
        print('(RB) was Released')
    if CliState<1 : CliState=1
    elif CliState>5 : CliState=5    
    return CliState 


def Thread1Script():
    time.sleep(1)
    GUI.run_webserver()
    return True

def Thread2Script():
    time.sleep(1)
    update_displays = True
    while(True):
        if update_displays == True:
            GUI.gcode_displaydata_fill(CncInterface)
            time.sleep(0.1)    
    return True   

def Thread3Script():
    time.sleep(0.1)
    CncInterface.run()
    return True

def Thread4Script():
    time.sleep(1)
    ControlerXbox.JoyHandler.initcontrol()
    BordcastControllState = 1
    ContrState = ControlerXbox.JoyHandler.UpdateControl() #first requisition
    while BordcastControllState == 1:
        ContrlastState = ContrState #reminding last state to perceive event
        ContrState = ControlerXbox.JoyHandler.UpdateControl()
        ClientNewState = ControlEvent(ContrState,ContrlastState)
        GUI.ClientState[1] = ClientNewState
        time.sleep(50/1000)
    return True

@etrogui.eel.expose
def UpdateClient():
    return GUI.gcode_display


Thread1 = threading.Thread(name='EtrOGUI server', target=Thread1Script)
Thread2 = threading.Thread(name='EtrOGUI handler', target=Thread2Script)
Thread3 = threading.Thread(name='CNC Machine Interface', target=Thread3Script)
Thread4 = threading.Thread(name='robot controll interface', target=Thread4Script)

Thread1.start()
Thread2.start()
Thread3.start()
#Thread4.start()
