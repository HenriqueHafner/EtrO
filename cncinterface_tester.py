# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import serialcncinterface
import time

machine_connected_tester = True
if machine_connected_tester == True:
    CNC_INTERFACE = serialcncinterface.serial_cnc_interface()
    CNC_INTERFACE.run()
    
    time.sleep(3)
    CNC_INTERFACE.serial_parse_buffer()
    CNC_INTERFACE.incomming_data_handler()
    CNC_INTERFACE.monitor_serial_update()
    print(CNC_INTERFACE.console_stdout_data[0:5])
    time.sleep(1)
    
    CNC_INTERFACE.gcode_custom_insert('temp')
    CNC_INTERFACE.gcode_status = 1
    CNC_INTERFACE.gcode_stream_handler()
    counter = 0
    while CNC_INTERFACE.feedback_status[0] == True:
        CNC_INTERFACE.serial_feedback_handler()
        counter += 1
    print(counter)
    print(CNC_INTERFACE.feedback_status)
    CNC_INTERFACE.incomming_data_handler()
    CNC_INTERFACE.monitor_serial_update()
    print(CNC_INTERFACE.console_stdout_data[0:5])
    
    CNC_INTERFACE.gcode_custom_insert('home',imediate=True)
    CNC_INTERFACE.gcode_data_handler()
    CNC_INTERFACE.gcode_set_data()
    CNC_INTERFACE.gcode_status = 2
    counter = 0
    while CNC_INTERFACE.gcode_data[1] < 197:
        CNC_INTERFACE.gcode_stream_handler()
        CNC_INTERFACE.monitor_serial_update()
        # print(CNC_INTERFACE.console_stdout_data[0])
        counter += 1
        time.sleep(0.05)
    print(CNC_INTERFACE.console_stdout_data)
    print(counter)
    
machine_not_connected_tester = False
if machine_not_connected_tester == True:
    tester = serialcncinterface.serial_cnc_interface()
    tester.run()

    # Tester for incomming serial data.
    tester.serial_parse_buffer()
    if tester.serial_buffed_data == '' : tester.serial_buffed_data = 'Tester arg1\nNo Serial Binded arg2\nG01 X23 Y43\nincomplete_message...'#.encode('utf-8')
    
    tester.incomming_data_handler() #take data from API Serial interface to program scope.
    tester.serial_buffed_data += 'abc\n'#.encode('utf-8')
    tester.incomming_data_handler() #take data from API Serial interface to program scope.


    data_to_write = 'Gtester X43.2 Y44.1'
    tester.write_cnc_serial(data_to_write)
    data_to_write = ';Invalid Command Tester'
    tester.write_cnc_serial(data_to_write)

    
    print(tester.serial_buffed_data)
    data_to_write = 'GFeedbackTest X43.2 Y44.1'
    tester.write_cnc_serial(data_to_write,feedback_check=True)
    tester.serial_buffed_data += 'ok\n'
    tester.write_cnc_serial('GToWrite',feedback_check=True)
    tester.write_cnc_serial('GToFail',feedback_check=True)
    tester.serial_buffed_data += 'ok\n'
    tester.serial_feedback_handler()

    tester.gcode_stream_handler()
    tester.gcode_custom_message = ['Gcustom','Message']
    tester.gcode_status = 1
    tester.gcode_stream_handler()
    tester.serial_buffed_data += 'ok\n'
    tester.gcode_stream_handler()
    tester.serial_buffed_data += 'ok\n'
    tester.gcode_stream_handler()

    for i in tester.datatable: print(i)
    
    tester.gcode_status = 2
    tester.monitor_cnc_update(return_data=False)    
    print(tester.monitor_data)








