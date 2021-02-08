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
    time.sleep(0.5)
    GUI.run()
    return True

def Thread2Script():
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

def Thread3Script():
    time.sleep(1)
    BroadcastControllState = 1
    CncInterface = serialcncinterface.SerialCNCInterface()
    CncInterface.run()
    while BroadcastControllState == 1:
        status = CncInterface.CNCStatus()
        etrogui.ClientState = [status[0],time.ctime()]
        print(etrogui.ClientState)
        time.sleep(0.5)
    return True

Thread1 = threading.Thread(name='EtrOGUI server', target=Thread1Script)
Thread2 = threading.Thread(name='robot controll interface', target=Thread2Script)
Thread3 = threading.Thread(name='CNC Machine Interface', target=Thread3Script)

Thread1.start()
#Thread2.start()
Thread3.start()

