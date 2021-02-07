# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:22:13 2020

@author: Henrique
"""

import threading
import time
import etroapp
import ControlerXbox
import sys

def ControlEvent(State,LastState):
    CliState=etroapp.ClientState[1]
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
    Etroapp = etroapp.etroapp()
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
        etroapp.ClientState[1] = ClientNewState
        time.sleep(50/1000)
        
    return True


Thread1 = threading.Thread(name='etroapp server', target=Thread1Script)
Thread2 = threading.Thread(name='robot interface', target=Thread2Script)

Thread1.start()
Thread2.start()



