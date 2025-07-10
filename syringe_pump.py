# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 12:12:36 2025

@author: csmpeo1
"""

import serial

class SyringePump():
       
    def __init__(self,port):      
        #initialize the serial port
        ser = serial.Serial()
        ser.port = port

        #serial settings
        ser.bytesize = serial.EIGHTBITS
        ser.stopbits = serial.STOPBITS_ONE
        ser.parity = serial.PARITY_NONE
        ser.xonxoff = True
        ser.baudrate = 19200

        #timeout so don't wait forever
        ser.timeout = 1

        #open serial port
        ser.open()        
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        #save serial port 
        self.ser = ser
        
    def send_command(self,cmd):    
        #flush buffers
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        
        #send command to get data
        command = cmd + '\r\n'
        self.ser.write(command.encode())
        
        return
    
    def start(self):
        self.send_command('run')
        return
    
    def stop(self):
        self.send_command('stp')
        return