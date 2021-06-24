# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 05:22:13 2020

@author: Henrique
"""

import threading
import time

import etrogui
import machineinterface
import serialasynchandler

machine_interface = machineinterface.machine_interface()
serialcom = serialasynchandler.serial_async_handler()
gui = etrogui.gui()


def THREAD_1_script():
    time.sleep(1)

    setup_done_flag = False
    while setup_done_flag == False:
        try:
            setup_done_flag = serialcom.setup_done
        except:
            None
        time.sleep(0.5)
        
    machine_interface.serial_handler_set_instance(serialcom)
    machine_interface.run()


def THREAD_2_script():
    time.sleep(1)

def THREAD_3_script():  
    serialcom.run()

def THREAD_4_script():
    time.sleep(1)   
    
    setup_done_flag = False
    while setup_done_flag == False:
        try:
            setup_done_flag = machine_interface.setup_done
        except:
            None
        time.sleep(0.5)
        
    gui.set_machine_interface(machine_interface)
    gui.run_webserver()

@etrogui.eel.expose
def update_terminal_gcode():
    try:
        data = gui.terminal_gcode_handler()
    except:
        data = ['Failed to get.']
    return data
@etrogui.eel.expose
def call_terminal_gcode(call_mesage):
    data = gui.terminal_gcode_caller(call_mesage)
    return data
@etrogui.eel.expose
def update_monitor_serial():
    try:
        data = gui.monitor_serial_handler()
    except:
        data = ['Failed to get.']
    return data
@etrogui.eel.expose
def update_monitor_machine():
    try:
        data = gui.monitor_machine_handler()
    except:
        data = ['Failed to get.']
    return data

THREAD_1 = threading.Thread(name='Machine Interface', target=THREAD_1_script)
THREAD_2 = threading.Thread(name='GUI Handler', target=THREAD_2_script)
THREAD_3 = threading.Thread(name='Serial Comunicator', target=THREAD_3_script)
THREAD_4 = threading.Thread(name='web server', target=THREAD_4_script)

THREAD_1.start()
# THREAD_2.start()
THREAD_3.start()
THREAD_4.start()
