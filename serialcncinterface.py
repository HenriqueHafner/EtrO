# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import serial
import serial.tools.list_ports as lp  # return a object list with serial ports information
import glob
import os

class serial_cnc_interface():

    def __init__(self):
        #serial communication attributes
        self.setup_done = False
        self.keep_looping = True
        self.SerialPorts = []
        self.serial_buffed_data = ''
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA'  # Arduino Clone Instance, reference hwid
        self.ControllerCOM = False  # var will be further overwrited with serial comunmicator instance
        self.ControllerPortName = str  # var with the part name 
        self.datatable_len = 30
        self.datatable = [[0,'way','message']]*self.datatable_len
        self.datatable_ipos = 0  # Position to insert new messages
        self.datatable_mindex = 0  # last message line number 
        self.feedback_status = [False,'index','message calling feedback ',
                                'index','feedback message',0]
        self.console_stdout_data = []
        self.monitor_data = []
        self.monitor_timestamp = 0

        #comand_file attributes
        self.gcode_status = 0
        self.gcode_custom_message = []
        self.gcode_data = [['0'], 5, 'Null', 0]  # [Gcode File, file line pos,file name, end of file line index]
        self.gcode_max_index_line = 0
        self.gcode_datas_dir = ['']
        self.gcode_data_name = 'Null'
        self.gcode_data_version = 'Null'
        self.gcode_data_adress = 'Null'
        self.gcode_datas_list = ['Null']

# Serial comunication methods

    def find_serial_device(self):
        self.SerialPorts = lp.comports()
        for i in self.SerialPorts:
            if i.hwid == self.Controller_hwid:
                self.ControllerPortName = i.name
                print('Found Serial port for Controler with ',self.Controller_hwid,' hwid')
                return True
        self.ControllerPortName = 'Null'
        return False

    def bind_communication(self):
        ControllerPortName = self.ControllerPortName
        if ControllerPortName != 'Null':
            self.ControllerCOM = serial.Serial(port=ControllerPortName,baudrate=250000,timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
            return True
        else:
            return False

    def serial_flush(self, buff=True):
        if not buff:
            self.ControllerCOM.reset_input_buffer()
            return True
        read_buff_size = self.ControllerCOM.in_waiting
        dump = self.cnc_interface_read_parser(read_buff_size)
        self.debug_out = dump
        flush_status = self.serial_message_buffer_insert(dump,'in')
        return flush_status

    def datatable_insert_data(self,data,label=''):
        """Insert data with label to the datatable list.
        """
        label = label[:5]
        if data == False:
            data = 'Invalid command.'
        if type(data) == bytes:
            data = data.decode('utf-8')
        if type(data) == str:
            data = [data]
        # from here, data must be a list of string messages.
        if type(data) != list:
            print("failed to assure 'data' is list()")
            return False
        ipos = self.datatable_ipos
        mindex = self.datatable_mindex
        for message_i in data:
            self.datatable[ipos] = [mindex,label,message_i]
            ipos += 1
            mindex += 1
            if ipos >= self.datatable_len-1:
                ipos = 0  #preventing out of range index
        self.datatable_ipos = ipos
        self.datatable_mindex = mindex
        return True

    def monitor_serial_update(self,return_data=True):
        datatable = sorted(self.datatable, reverse=True)
        stdout_data_l = []
        for message in datatable:
            nessage_str = message[1]+message[2]
            if len(nessage_str) >= 80:
                nessage_str = nessage_str[0:75]
                nessage_str += ('[...]')
            stdout_data_l.append(nessage_str)
            if len(stdout_data_l) >= 10:
                break
        if return_data == True:
            return stdout_data_l
        else:
            self.console_stdout_data = stdout_data_l
            return True

    def monitor_cnc_update(self,return_data=True):
        if time.time() - self.monitor_timestamp > 0.5:
            self.monitor_timestamp = time.time()
            if len(self.gcode_custom_message) == 0:
                self.gcode_custom_insert('temp')
        
        monitor_data_app_l = []
        monitor_data_app_l += ['file: '+self.gcode_data_name+' version: '+self.gcode_data_version]
        monitor_data_app_l += [self.monitor_get_status('M105\n','T:')]
        self.monitor_data = monitor_data_app_l
        if return_data == True:
            return self.monitor_data
        return True

    def monitor_get_status(self,command,feedback_key):
        datatable = sorted(self.datatable, reverse=True)
        if len(self.gcode_custom_message) == 0:
            self.gcode_custom_message.append(command)
        for entry in datatable: # esta pegando o ultimo em datatable e nao o mais recente
            if entry[1].count('r') > 0 and entry[2].count(feedback_key) > 0:
                return entry[2]

        return False
                
        

    def serial_parse_buffer(self): 
        """ take data from serial API buffer and copy it to memory scope buffer
        The transposed data is ereased from source serial API buffer.
        """
        #check if binded
        if self.ControllerCOM == False:                
            print('No serial device binded.')
            return False
        data = ''
        readbuffer_size = self.ControllerCOM.in_waiting  # keep reading buffer until have less than this.
        while readbuffer_size > 0:
            data_piece = self.ControllerCOM.read(readbuffer_size)
            data_piece = data_piece.decode('utf-8')
            data += data_piece
            if readbuffer_size > 850: #buffer was full
                time.sleep(0.1) # give some time to incomming data
            readbuffer_size = self.ControllerCOM.in_waiting
        self.serial_buffed_data += data
        return True

    def incomming_data_handler(self):
        '''
            it recoganizes messages with '\n' ending from serial_buffed_data 
            and inserts it in datatable
        '''
        serial_buffed_data_l = self.serial_buffed_data
        messages = []
        message_piece = ''
        for char in serial_buffed_data_l:
            if char == '\n':
                message_piece += '\n'
                if len(message_piece) < 2:
                    print('unexpected state of serial_buffed_data')
                    return False
                messages.append(message_piece)
                message_piece = ''
            else:
                message_piece += char
        if len(messages) > 0:  # messages found
            self.datatable_insert_data(messages,'[r ]:')
        # if len(message_piece) > 0:  # residue in buffer with no '\n'
        self.serial_buffed_data = message_piece  
        return True

    def write_cnc_serial(self,data,data_conditioner=True,feedback_check=False):
        if self.feedback_status[0] == True:
            self.serial_feedback_handler()
            if self.feedback_status[0] == True:
                print('Unable to write, still waiting for feedback')
                print(self.feedback_status)
                self.datatable_insert_data(data,'fail!')
                return False
        
        if data_conditioner == True: #condictioning data
            data = self.gcode_message_conditioner(data)
        label='[w ]:'
        
        if data is not False:
            #feedback listener
            if feedback_check == True:
                label='[wf]:'
                self.feedback_status[0] = True
                self.feedback_status[2] = data
                self.feedback_status[5] = time.time()
            #  check output cue
        
        if self.ControllerCOM == False: #serial availability checkpoint
            print('Write: ',data,' no device binded to write.')
        else:
            self.ControllerCOM.write(data) #write data
        self.datatable_insert_data(data,label)
        return True

    def serial_feedback_handler(self):
        # implement datatable correlation
        if self.feedback_status[0] == True:
            self.serial_parse_buffer()
            if self.serial_buffed_data.rfind('ok') > -1:
                self.incomming_data_handler()
                self.feedback_status[0] = False
                return False
            else:
                if time.time() - self.feedback_status[5] > 30:
                    self.feedback_status[0] = False
                    self.feedback_status[4] = 'No feedback recieved'
                    print('feedback timeout')
                    return False
                return True
        else:
            return False  # True means keep wating for feedback.

#  Gcode methods

    def gcode_message_conditioner(self,message):
        acceptable_command = ['G', 'M'] #Check if message is a valid command
        is_valid_command = False
        for i in acceptable_command:
            if message[0] == i:
                is_valid_command = True
                break
        if is_valid_command == False:
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
        self.gcode_max_index_line = len(self.gcode_data[0])-1
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
        self.gcode_datas_dir = gcode_datas_dir_l
        self.gcode_datas_list = gcode_datas_list_l
        self.gcode_set_data()       
        return True

    def gcode_stream_handler(self):
        if self.feedback_status[0] == True:
            self.serial_feedback_handler()
            return False
        if self.gcode_status >= 1:
            if len(self.gcode_custom_message) > 0:
                self.write_cnc_serial(self.gcode_custom_message.pop(0),
                                      feedback_check=True)
                return True
            if self.gcode_status == 2:
                self.gcode_stream()
        return True

    def gcode_stream(self):
        gc_line_pos = self.gcode_data[1]
        gc_linebwrite = self.gcode_data[0][gc_line_pos]
        write_status = self.write_cnc_serial(gc_linebwrite,
                                             feedback_check=True)
        if write_status == True:
            if self.gcode_data[1] >= self.gcode_max_index_line:
                self.gcode_status = 1
                return True
            self.gcode_data[1] +=1
            return True
        else:
            return False
    
    def gcode_move_lastlinepos(self,line,operator='abs'):
        curr_line = self.gcode_data[1]
        target_line = None
        if operator == 'abs':
            target_line = line
        elif operator == 'relative':
            target_line = curr_line+line
        if target_line < 0:
            print('requested target_line was negative. Going to 0 instead')
            target_line = max(0,target_line)
        self.gcode_data[1] = target_line
        return True
        
    def gcode_custom_insert(self,command):
        commands = [['home','G28 X Y\n'],['stepper_d','M84\n'],
                    ['warm_n','M104 S235\n'],['warm_b','M140 S90\n'],
                    ['cool_n','M104 S0\n'],['cool_b','M140 S0\n'],
                    ['stats','M105\n'],
                    ['move+n',],['move_c1',],
                    ['move_c2',],['move_c3',],
                    ['move-z',],['move+z',],
                    ]
        for i in commands:
            if command == i[0]:
                self.gcode_custom_message.append(i[1])
                return True
                break
        return False

# Operation methods
    def loop(self):
        while 1:
            self.serial_parse_buffer()
            self.gcode_stream_handler()
            time.sleep(0.02)
            if self.keep_looping == False:
                return True
        return True

    def run(self):
        self.find_serial_device()
        self.bind_communication()
        self.gcode_data_handler('GetNewest','C:\\Casa Modelos\\Printing Files')
        self.setup_done = True
        self.keep_looping = True
        self.gcode_status = 1
        self.loop()
        return True

























