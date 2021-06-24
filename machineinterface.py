# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import glob
import os
import marlin_gcode_toolbox

class machine_interface():

    def __init__(self):
        #machine controller attributes
        self.serial_handler = object
        self.machine_interface_mode = 0  # 0 is idle state
        self.setup_done = False
        self.command_write_queue = []
        self.feedback_timestamp = 0
        self.monitor_timestamp = 0
        self.datatable = []
        
        #comand_file attributes, gcode
        self.gcode_data = [['0'], 5, 'Null', 0]  # [Gcode File, file line pos,file name, end of file line index]
        self.gcode_data_name = 'Null'
        self.gcode_data_version = 'Null'
        self.gcode_data_adress = 'Null'
        self.gcode_dir = ['']
        self.gcode_list = ['Null']

        self.gcode_feedbackneeded_list = [
            'G0','G1','G00','G01','M105','M109','M190','M400'
            ]
        self.gcode_notfeedback_list = [
            ]
        self.gcode_log_failedfeedback = []

    def serial_handler_set_instance(self,serial_handler_l):
        self.serial_handler = serial_handler_l

    def monitor_machine_update(self,return_data=True):
        if time.time() - self.monitor_timestamp > 2:
            self.monitor_timestamp = time.time()
            write_cue = self.command_write_queue
            if len(write_cue) == 0:
                self.command_custom_insert('stats')
            elif len(write_cue) == 1 and write_cue[0][:4] != 'M105':
                self.command_custom_insert('stats')

        datatable_l = self.datatable_update(size=30,return_only=True)
        datatable_l.reverse()
        monitor_data_app_l = []
        
        temp_status = ['Failed to find a response in datatable']
        for message in datatable_l:
            if message[1][1] == 'r' and message[2].rfind('T:') > 0:
                temp_status = message[2][3:]
                break
        monitor_data_app_l.append(temp_status)

        monitor_data_app_l.append('file: '+self.gcode_data_name+
                                  ' version: '+self.gcode_data_version)
        monitor_data_app_l.append('Machine mode: '+str(self.machine_interface_mode))
        monitor_data_app_l.append('Command queued to write.')
        
        for command in self.command_write_queue[0:5]:
            monitor_data_app_l.append(command)
        len_queued = len(self.command_write_queue)
        if len_queued > 5:
            monitor_data_app_l += ['[...] More:',str(len_queued-5)]
        self.monitor_data = monitor_data_app_l
        if return_data == True:
            return self.monitor_data
        else:
            return None
        return ['none','none']

    def monitor_serial_update(self):
        return self.serial_handler.monitor_serial_update()
    
#  Gcode methods
    def gcode_message_conditioner(self,message):
        acceptable_command = ['G', 'M'] #Check if message is a valid command
        is_valid_command = False
        for i in acceptable_command:
            if message[0] == i:
                is_valid_command = True
                break
        if is_valid_command == False:
            print('invalid command: ',message)
            return False      
        if message[-1] != '\n': #Force a line break at end
            message = message+'\n'
        message = bytes(message,'utf-8') #encode to bytes
        return message

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

    def gcode_data_handler(self,arg_def='GetNewest',gcode_datas_dir_l='None'):#pick a gcode file
        if gcode_datas_dir_l == 'None':
            gcode_datas_dir_l = os.getcwd()

        if arg_def == 'test':
            gcode_data_name_l = 'test.gcode' # _l means a local scope var of instance propertie.
            gcode_datas_list_l = glob.glob(os.path.join(gcode_datas_dir_l,
                                                        '*.gcode'))
        elif arg_def == 'GetNewest':
            gcode_datas_list_l = glob.glob(os.path.join(gcode_datas_dir_l,
                                                        '*.gcode'))
            gcode_datas_list_l.sort(key=os.path.getctime,reverse=True)
            target_file_index = gcode_datas_list_l[0].rindex('\\') #finding star position of file name string.
            gcode_data_name_l = gcode_datas_list_l[0][target_file_index+1:] #extracting the file_name from path
        elif type(arg_def) == list: #set a path in index 0 and file name in index 1
            gcode_data_name_l = arg_def[1]
            gcode_datas_dir_l = arg_def[0]           
            gcode_datas_list_l=[os.path.join(gcode_datas_dir_l, 
                                             gcode_data_name_l)]
        else:
            print('Unexpected arg_def argument.')
            return False

        self.gcode_data_adress = os.path.join(gcode_datas_dir_l,
                                              gcode_data_name_l)
        self.gcode_data_name = gcode_data_name_l
        self.gcode_data_version = os.path.getctime(self.gcode_data_adress)
        self.gcode_data_version = time.ctime(self.gcode_data_version)[4:16]
        self.gcode_dir = gcode_datas_dir_l
        self.gcode_list = gcode_datas_list_l
        self.gcode_set_data()       
        return True

    def machine_writer_handler(self):
        if self.feedback_waiting() is True:  #check if  should w8 for feedback
            return False
        command = None
        mstats = self.machine_interface_mode
        
        if len(self.command_write_queue) == 0 and mstats >=2:
            command = self.gcode_stream()
            if command is False:  # unable to stream a command
                self.machine_interface_mode = 1
                print('No command to stream, machine_interface_mode set to 0')
                return True
            else:
                self.command_write_queue.append(command)
        
        if len(self.command_write_queue) >= 1 and mstats >= 1:
            writing_flag = self.write_command_serial(self.command_write_queue[0])
            if writing_flag is True:
                self.command_write_queue.pop(0)
                return True
            
        if len(self.command_write_queue) == 0:
            return True
        
        print('machine_interface_mode:',self.machine_interface_mode
              ,'command_write_queue :',self.command_write_queue)
        return False

    def feedback_waiting(self):
        data = self.datatable_update(size=1,return_only=True)
        last_message = data[-1]
        if last_message[1][1] == 'w':
            fb_flag = self.check_feedback_needed(last_message[2])
            if fb_flag == 0:
                return False
            elif fb_flag == 1:
                return True
            elif fb_flag == 2:
                if time.time() - self.feedback_timestamp > 1:
                    self.log_failedfeedback(last_message[2])
                    print('No feedback for:',last_message[2])
        return False  # True means keep wating for feedback.
    
    def check_feedback_needed(self,message:str):  # Especific to 3D printer
        '''
        Parameters
        ----------
        message : str
            past writed message to extract command and analize.
        Returns
        -------
        0
            Recoganized command, no need of feedback.
        1
            Recoganized command, needs feedback.
        2
            Unrecoganized command, needs feedback.
        '''
        gcode = self.message_exctract_gcode(message)
        for i in self.gcode_notfeedback_list:
            if i == gcode:
                return 0
        for i in self.gcode_feedbackneeded_list:
            if i == gcode:
                return 1
        return 2

    def log_failedfeedback(self,message:int):
        ''' log gcode message in instance propertie
        '''
        gcode = self.message_exctract_gcode(message)
        for i in self.gcode_log_failedfeedback:
            if i == gcode:
                return None
        self.gcode_log_failedfeedback.append(gcode)
        print('Logged feedback fail for:',gcode)
        
    def message_exctract_gcode(self,message:int):
        ''' recoganize and return gcode until first space character
        '''
        gcode = ''
        for char in message:
            if char == ' ':
                break
            gcode += char
        return gcode
        
    def datatable_update(self,size=6,return_only:bool=False):
        datatable_l = self.serial_handler.get_datatable(size)
        if return_only:
            return datatable_l
        self.datatable = datatable_l

    def write_command_serial(self,command:str):
        command_conditioned = self.command_conditioner(command)
        if isinstance(command_conditioned,bytes):
            write_flag = self.serial_handler.write_serial(command_conditioned)
            if write_flag is True:
                self.feedback_timestamp = time.time()  # timestamp to check if feedback waiting time
                return True  # sucessful writed
            else:
                return False  # unsuccessful writed
        elif command_conditioned is False:
            return True  # ignoring commands conditioned to False
        else:
            print('unexpectated command_conditioned.',command_conditioned)
        return True
    
    def command_conditioner(self,command:str):  # 3D printer especifics
        acceptable_command = ['G', 'M'] #Check if message is a valid command
        is_valid_command = False
        for i in acceptable_command:
            if command[0] == i:
                is_valid_command = True
                break
        if is_valid_command == False:
            print('invalid command: ',command)
            return False 
        if command.rfind(';') > 0:
            command = command.split(';')[0]
        if command[-1] == ' ':
            command = command[:-1]
        if command[-1] != '\n': #Force a line break at end
            command = command+'\n'
        command = bytes(command,'utf-8') #encode to bytes
        return command

    def gcode_stream(self):
        """ return the current line of gcode and increment line position.
            return False if line position exceeds gcode_data line number
        """
        if self.gcode_data[1] > self.gcode_data[3]:  #Checking if achieved end of gcode file.
            return False
        gc_line_pos = self.gcode_data[1]
        gc_linebwrite = self.gcode_data[0][gc_line_pos]
        self.gcode_data[1] +=1
        return gc_linebwrite

    def gcode_move_lastlinepos(self,line:int,relative:bool=True):
        '''shift or set position line.
        Parameters
        ----------
        line : int
            desired shift in line position or new absolute line position.
        relative : bool, optional
            Pass False if the line is not a relative shift from atual line.
            The default is True.
        Returns
        -------
        bool
            True if the line can be set. False if line is 
            greater than last line or smaller than zero.

        '''
        curr_line = self.gcode_data[1]
        if relative:
            target_line = curr_line+line
        else:
            target_line = line
        if target_line < 0:
            print('requested target_line was negative.')
            return False
        if target_line > self.gcode_data[3]:  # check if target line exceeds file
            print('requested target_line is greater than last line.')
            return False
        self.gcode_data[1] = target_line
        return True
        
    def gcode_check_flag(self):
        curr_line = self.gcode_data[1]
        next_mesage = self.gcode_data[0][curr_line]
        if next_mesage == (';LAYER:1'):
            self.machine_interface_mode = 1
        else:
            return False
        return True

    def command_custom_insert(self,function):
        for i in marlin_gcode_toolbox.function_table:
            if function == i[0]:
                commands = i[1:]
                self.command_write_queue += commands
                return True
        return False

    def set_interface_mode(self,state:int):
        self.machine_interface_mode = state
    
    def terminal_gcode_caller(self,call_message):
        if call_message == 'setup':
            commands = ['WriteBuffer','StreamGcode','ReloadGecode']
            for func in marlin_gcode_toolbox.function_table:
                commands.append(func[0])
            return commands
        elif call_message == 'WriteBuffer':
            self.machine_interface_mode = 1
        elif call_message == 'StreamGcode':
            self.machine_interface_mode = 2
        elif call_message == 'ReloadGecode':
            self.gcode_data_handler('GetNewest','C:\\Casa Modelos\\Printing Files')
        elif isinstance(call_message,str):
            self.command_custom_insert(call_message)
            

# Operation methods
    def loop(self):
        while True:
            if self.machine_interface_mode >= 1:
                self.machine_writer_handler()
                self.gcode_check_flag()
            time.sleep(0.05)
        return True

    def run(self):
        self.gcode_data_handler('GetNewest','C:\\Casa Modelos\\Printing Files')
        self.setup_done = True
        self.loop()
        return True





















