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
        self.SerialPorts = []
        self.serial_buffed_data = ''
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA'  # Arduino Clone Instance, reference hwid
        self.ControllerCOM = False  # var will be further overwrited with serial comunmicator instance
        self.ControllerPortName = str  # var with the part name 
        self.datatable_len = 30
        self.datatable = [[0,'','']]*self.datatable_len
        self.datatable_ipos = 0  # Position to insert new messages
        self.datatable_mindex = 0  # last message line number 
        self.console_stdout_data = ['']*11
             
        #comand_file attributes
        self.gcode_status = 0
        self.gcode_custom_message = []
        self.gcode_data = [['0'], 5, 'Null', 0]  # [Gcode File, file line pos,file name, end of file line index]
        self.gcode_datas_dir = ['']
        self.gcode_data_name = 'Null'
        self.gcode_data_adress = 'Null'
        self.gcode_datas_list = ['Null']

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
        if type(data) == bytes:
            data = data.decode('utf-8')
        if type(data) == str:
            data = data.split('\n')
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

    def console_data_insert(self, data, label = ''):
        if type(data) == str:
            data = [data]
        elif type(data) == bytes:
            data = data.decode('utf-8')
            data = data.split('\n')
        for data_str in data:
            data_str = label+data_str
            if len(data_str) >= 80:
                data_str = data_str[0:75]
                data_str += ('[...]')
            self.console_stdout_data.append(data_str)
            del self.console_stdout_data[0]
        return True

    def serial_parse_buffer(self): 
        """ take data from serial API buffer to memory scope buffer
        """
        #check if binded
        if self.ControllerCOM == False:                
            print('No serial device binded.')
            return False
        data = ''
        readbuffer_size = self.ControllerCOM.in_waiting  # keep reading buffer until have less than this.
        while readbuffer_size >= 0:
            data_piece = self.ControllerCOM.read(readbuffer_size)
            data_piece = data.decode('utf-8')
            data += data_piece
            if readbuffer_size > 850: #buffer was full
                time.sleep(0.1) # give some time to incomming data
            readbuffer_size = self.ControllerCOM.in_waiting
        self.serial_buffed_data += data
        return True
    
    def incomming_data_hadler(self):
        '''
        Returns
        -------
        bool
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
            self.datatable_insert_data(messages)
        if len(message_piece) > 0:  # residue in buffer with no '\n'
            self.serial_buffed_data = message_piece
        return True
            
            
            
        self.datatable_insert_data(messages,'[r]:')

        return True
    
    def serial_feedback_handler(self):
        # feedback = False
        # feedback_timeout = 1
        # # feedback waiting block
        # if feedback != False:  
        #     rear = True
        #     stime = time.time()
        #     while rear == True:
        #         message = self.cnc_interface_read_parser(len(feedback))
        #         if debug == True: print(message)
        #         if message == feedback:
        #             rear = False
        #             return True
        #         elif len(message) > 0:
        #             message = message+self.cnc_interface_read_parser(1024)
        #             print(message)
        #             print('recieved feedback message is not the expected flag.')
        #             rear = False
        #             return False
        #         elif time.time()-stime > feedback_timeout:
        #             rear = False
        #             return 'Timeout, '+str(feedback_timeout)+' seconds with no respose.'
        #         time.sleep(0.02)
        return True
  
      
    def write_cnc_serial(self,data,data_conditioner=True,feedback_check=True):
        if self.ControllerCOM == False: #serial availability checkpoint
            print('Missing serial Device. ',data)
            return False          
        if data_conditioner == True: #condictioning data
            data = self.gcode_message_conditioner(data)
        

        self.cnc_interface_write_parser(data) #write data

        #feedback listener
        if feedback_check == True:
            feedback_message = bytes('ok\n','utf-8')
            sucess_flag = self.serial_read(feedback=feedback_message,
                                             char_limit=len(feedback_message))
            if sucess_flag == True:
                return True
            else:
                return False
        else:
            return True

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
    
    def CNCStatus(self):
        status = 'Null'
        try:
            self.ControllerCOM.flush()
            self.ControllerCOM.write(bytes("M105\n","utf-8"))
            status=self.serial_read()
        except AttributeError:
            status = 'Failed to comunicate.'
        return status

    def close(self):
        self.ControllerCOM.close()
        return True

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

    def gcode_data_handler(self,arg_def='test',gcode_datas_dir_l='None'):#pick a gcode file
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
        
        self.gcode_data_name = gcode_data_name_l
        self.gcode_datas_dir = gcode_datas_dir_l
        self.gcode_datas_list = gcode_datas_list_l
        self.gcode_data_adress = os.path.join(gcode_datas_dir_l,gcode_data_name_l)
        return True

    def gcode_stream_handler(self): #flush not working!!!
        if self.gcode_custom_message != []:
            for custom_message in self.gcode_custom_message:
                self.write_cnc_serial(custom_message)
                self.gcode_custom_message = []
        if self.gcode_status == 0:
            return True
        elif self.gcode_status == 1:
            self.gcode_stream()
            return True
        elif self.gcode_status == 2:
            while self.gcode_status == 2:
                self.gcode_stream()
                return True
        else:
            return False

    def gcode_stream(self):
        gc_line_pos = self.gcode_data[1]
        gc_linebwrite = self.gcode_data[0][gc_line_pos]
        self.gcode_data[1] +=1
        if gc_linebwrite[0] == ';':
            return 'Not valid command line'
        self.write_cnc_serial(gc_linebwrite)
        return True 
    
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
        
    def gcode_custom_insert(self,command,imediate=False):
        commands = [['home','G28 X Y\n'],['stepper_d','M84\n'],['warm_n','M104 S235\n'],['warm_b','M140 S90\n'],['cool_n','M104 S0\n'],['cool_b','M140 S0\n'],['temp','M105\n']]
        if type(command) == str:
            command = [command]
        for i in command:
            for j in commands:
                if i == j[0]:
                    if imediate == True:
                        self.write_cnc_serial(j[1])
                    else:
                        self.gcode_custom_message.append(j[1])
                    break
        return True
        
                
    
    def run(self):
        self.find_serial_device()
        self.bind_communication()
        self.gcode_data_handler('GetNewest')
        self.gcode_set_data()
        self.setup_done = True


#quando recarregado, file_handler nao atualiza as propriedades gcode_data
test = True
if test == True:
    tester = serial_cnc_interface()
    #tester.gcode_custom_message = ['G1 F480 X101.084 Y92.419','G1 X101.379 Y92.547','G1 X103.682 Y92.844','G1 X104.345 Y92.969','G1 X104.989 Y93.173','G1 X105.604 Y93.45','G1 X106.182 Y93.799','G1 X106.557 Y94.08','G1 X107.164 Y94.287','G1 X107.958 Y94.685','G1 X109.303 Y95.497','G1 X109.387 Y95.524','G1 X110 Y95.805','G1 X110.576 Y96.157','G1 X111.011 Y96.5','G1 F480 X101.084 Y92.419','G1 X101.379 Y92.547','G1 X103.682 Y92.844','G1 X104.345 Y92.969','G1 X104.989 Y93.173','G1 X105.604 Y93.45','G1 X106.182 Y93.799','G1 X106.557 Y94.08','G1 X107.164 Y94.287']
    tester.run()
    # flushed = False
    # while flushed == False:
    #     flushed = tester.serial_read(flush=True) #wait until read buffer is flushed in OS api.
    tester.serial_buffed_data = 'command1 arg1\ncommand2 arg2\ntestesteste123123\n; teste teste\ncommand3 xyz\nincomp...'#.encode('utf-8')
    #tester.datatable_insert_data(serial_read_ex,'[r]:')
    #tester.console_data_insert(serial_read_ex,'[r]:')
    tester.incomming_data_hadler()
    #tester.write_cnc_serial('G28 X Y')
    #tester.gcode_stream_handler()
     









