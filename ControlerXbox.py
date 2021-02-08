# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:22:17 2019

@author: henrique.ferreira
"""

import pygame
import time

class JoyHandler():
    pygame.display.init()
    pygame.joystick.init()
    
    def initcontrol(joy=0):
        global init 
        init = False
        if pygame.joystick.Joystick(joy).get_init == False:
            pygame.joystick.Joystick(joy).init()
            # Prints the joystick's name
            JoyName = pygame.joystick.Joystick(joy).get_name()
            print("Name of the joystick:")
            print(JoyName)
            return True
        else:
            return False
    
    
    def UpdateControl(joy=0,printData=False):
        pygame.event.pump()
    
        #Axis
        axis = [0.00]*6
        for i in range(6):
            axis[i] = round(pygame.joystick.Joystick(joy).get_axis(i),2)
        #buttons
        buttons = [0]*11
        for i in range(len(buttons)):
            buttons[i]=pygame.joystick.Joystick(joy).get_button(i)
        #hat
        hat = list(pygame.joystick.Joystick(joy).get_hat(0))
        
        if printData == True:
            print('Axis L LT R RT',axis)
            print('Butons',buttons)
            print('Hat',hat)
        
        return [axis,buttons,hat]
            
