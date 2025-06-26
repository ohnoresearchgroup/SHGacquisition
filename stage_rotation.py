# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 14:07:27 2025

@author: peo0005
"""

from pylablib.devices import Thorlabs

# Replace with actual serial number or COM port (e.g., "COM3")
DEVICE_ID = "55525624"

# Connect to the K10CR2 stage
try:
    stage = Thorlabs.KinesisMotor(DEVICE_ID)
except Exception as e:
    print(f"Failed to connect: {e}")
    exit()


#run forever
stage.jog("+")


#stop
stage.stop() 


#get homing parameters
stage.get_jog_parameters(channel=None, scale=False)


#returned velocity=73300775 for full speed

stage.setup_jog(max_velocity=7330077)