# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 13:36:17 2021

@author: localadmin
"""

function_table = [
['home_xy','G28 X Y\n'],['home_z','G28 Z\n'],
['stepper_d','M84\n'],['stats','M105\n'],
['warm_n','M104 S235\n'],['warm_b','M140 S90\n'],
['cool_n','M104 S0\n'],['cool_b','M140 S0\n'],
['move_c1','G0 X10 Y30\n'],
['move_c2','G0 X85 Y160\n'],
['move_c3','G0 X160 Y30\n'],
['move-z','G91\n','G1 Z-0.05','G90\n'],
['move+z','G91\n','G1 Z0.05','G90\n'],
['move+e','G91\n','G0 E1 F100','G90\n'],
['wait','M400'],
]