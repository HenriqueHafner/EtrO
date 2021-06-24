# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""
import time
import serial
import serial.tools.list_ports as lp  # return a object list with serial ports information

class serial_async_handler():

    def __init__(self):
        #serial communication attributes
        self.setup_done = False
        self.SerialPorts = []
        self.serial_buffed_data = ''
        self.Controller_hwid = 'USB VID:PID=0403:6001 SER=AK006ZRFA'  # Arduino Clone Instance, reference hwid
        self.ControllerCOM = object  # var will be further overwrited with serial comunmicator instance
        self.ControllerPortName = 'Null'  # Port Name 
        self.datatable_len = 99
        self.datatable = [[0,'label','message']]*self.datatable_len
        self.datatable_ipos = 0  # Position to insert new messages
        self.datatable_mcounter = 0  # message counter
        self.monitor_data = []
        self.monitor_timestamp = 0

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
        if ControllerPortName == 'Null':
            return False
        else:
            self.ControllerCOM = serial.Serial(port=ControllerPortName,
                                               baudrate=250000, timeout=1)
            print('Port: ',ControllerPortName, 'connected.')
            return True

    def write_serial(self,data,label='[w ]:'):
        """ write data in binded serial device, if there is one.
        """
        if self.ControllerCOM == False: #serial availability checkpoint
            print('Fail to write: ',data,' no device binded to write.')
            return False
        else:
            try:
                self.ControllerCOM.write(data) #write data
                self.datatable_insert_data(data,label)
                return True
            except:
                print('ControllerCOM failed to write.')
                return False

    def incomming_data_handler(self):
        """it recoganizes messages with '\n' ending from serial_buffed_data 
            and inserts it in datatable
        """
        new_data_flag = self.buffer_getnparse()
        if new_data_flag is False:  # nothing to do.
            return True
        serial_buffed_data_l = self.serial_buffed_data
        messages = []
        message_piece = ''
        for char in serial_buffed_data_l:  # looking char by char for frase stop char.
            if char == '\n':
                message_piece += '\n'
                if len(message_piece) < 2:
                    print('empty message in serial_buffed_data')
                    return True
                messages.append(message_piece)
                message_piece = ''
            else:
                message_piece += char
        if len(messages) > 0:  # messages found
            for msg in messages:
                self.datatable_insert_data(msg,'[r ]:')
        self.serial_buffed_data = message_piece  
        return True

    def buffer_getnparse(self): 
        """ takes data from serial API buffer and copy it to memory scope buffer
        The transposed data is ereased from source serial API buffer.
        """
        readbuffer_size = self.ControllerCOM.in_waiting  # keep reading buffer until have less than this.
        if readbuffer_size == 0:
            return False
        data = ''
        while readbuffer_size > 0:
            data_piece = self.ControllerCOM.read(readbuffer_size)
            data_piece = data_piece.decode('utf-8')
            data += data_piece
            if readbuffer_size > 850: #buffer was full
                time.sleep(0.05) # give some time to incomming data
            readbuffer_size = self.ControllerCOM.in_waiting
        self.serial_buffed_data += data
        return True

    def datatable_insert_data(self, data:[bytes,str], label: str=''):
        """Inserts data in datatable.
        """
        label = label[:5]
        if isinstance(data,bytes):
            data = data.decode('utf-8')
            data = [data]
        elif isinstance(data,str):
            data = [data]
        # from here, data must be a list of string messages.
        elif not isinstance(data,list):
            print("failed to assure 'data' as list()")
            return False
        ipos = self.datatable_ipos
        mcounter = self.datatable_mcounter
        for message_i in data:
            self.datatable[ipos] = [mcounter,label,message_i]
            ipos += 1
            mcounter += 1
            if ipos >= self.datatable_len:  #preventing out of range index
                ipos = 0
        self.datatable_ipos = ipos
        self.datatable_mcounter = mcounter
        return True

    def monitor_serial_update(self,return_data=True):
        '''fill monitor_data with formated data from datatable to show in 
        serial monitor.
        Parameters:
        ----------
        return_data : bool, optional
            True to return data, False to just update.
        Returns:
        -------
        monitor_data_l : list
            return updated monitor_data_l
        True : bool
            store updated data in serial_async_handler.monitor_data
        '''
        size = 20
        datatable = self.get_datatable(size)
        monitor_data_l = []
        for message in datatable:
            nessage_str = message[1]+message[2]
            if len(nessage_str) >= 80:
                nessage_str = nessage_str[0:75]
                nessage_str += ('[...]')
            monitor_data_l.append(nessage_str)
            if len(monitor_data_l) >= size:
                break
        if return_data == True:
            return monitor_data_l
        else:
            self.monitor_data = monitor_data_l
            return True

    def get_datatable(self, size):
        if size > self.datatable_len:
            size = self.datatable_len - 1
        self.incomming_data_handler()
        msg_pos = self.datatable_ipos - 1
        datatable_l = []
        for i in range(size):
            datatable_l.append(self.datatable[msg_pos])
            msg_pos += -1
        return datatable_l

    def serial_dump(self):
        self.ControllerCOM.reset_input_buffer()
        return True
    
    def serial_close(self):
        try:
            self.serial.Serial.close()
            time.sleep(1)
            self.__init__()
            return True
        except:
            return False

    def run(self):
        if not self.setup_done:
            self.find_serial_device()
            self.bind_communication()
            self.setup_done = True
            return True
        else:
            return False























