# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:22:13 2020

@author: Henrique
"""

import threading
import time

import etrogui
import serialcncinterface

GUI = etrogui.gui()
CNC_INTERFACE = serialcncinterface.serial_cnc_interface()

def control_event(State,LastState):
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


def THREAD_1_script():
    time.sleep(1)
    GUI.run_webserver()
    return True

def THREAD_2_script():
    time.sleep(1)
    update_displays = True
    while(True):
        if update_displays == True:
            GUI.gcode_displaydata_fill(CNC_INTERFACE)
            time.sleep(0.1)
    return True 

def THREAD_3_script():
    time.sleep(0.1)
    CNC_INTERFACE.run()
    return True

def THREAD_4_script():
    # time.sleep(2)
    # import ControlerXbox
    # ControlerXbox.JoyHandler.initcontrol()
    # BordcastControllState = 1
    # ContrState = ControlerXbox.JoyHandler.UpdateControl() #first requisition
    # while BordcastControllState == 1:
    #     ContrlastState = ContrState #reminding last state to perceive event
    #     ContrState = ControlerXbox.JoyHandler.UpdateControl()
    #     ClientNewState = ControlEvent(ContrState,ContrlastState)
    #     gui.ClientState[1] = ClientNewState
    #     time.sleep(50/1000)
    return True

@etrogui.eel.expose
def update_client():
    return GUI.gcode_display

@etrogui.eel.expose
def serial_console_monitor():
    if len(CNC_INTERFACE.console_stdout_buffer) == 0:
        return True
    else:
        message = CNC_INTERFACE.console_stdout_buffer[0]
        del CNC_INTERFACE.console_stdout_buffer[0]
    return message


THREAD_1 = threading.Thread(name='EtrOGUI server', target=THREAD_1_script)
THREAD_2 = threading.Thread(name='EtrOGUI handler', target=THREAD_2_script)
THREAD_3 = threading.Thread(name='CNC Machine Interface', target=THREAD_3_script)
THREAD_4 = threading.Thread(name='robot controll interface', target=THREAD_4_script)

THREAD_1.start()
THREAD_2.start()
THREAD_3.start()
#THREAD_4.start()
