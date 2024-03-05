"""! @file thermal_cam.py
  
  This file uses I2C communication to talk with 
  
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """
  
#import relavant modules 
from pyb import I2C
from pyb import Pin
import utime
import struct

#create an I2C object with mode I2C.CONTROLLER 
obj = I2C(1, I2C.CONTROLLER, baudrate = 100000)
print(obj.scan())                   # Check for devices on the bus
# obj.mem_write('\x0C', 0x28, 0x3D)   # Send a 7 to sensor at 0x28, register 0x3D
# utime.sleep(1)