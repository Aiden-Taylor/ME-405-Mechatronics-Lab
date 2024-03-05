"""! @file bno_test.py
  
  This file uses I2C communication to talk with an IMU at hex address 28 and reads
  the Euler angles that are stored in the registers 1A - 1F and scales those values
  by 1/16 to print out the pitch, yaw, and roll angles.
  
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

from pyb import I2C
from pyb import Pin
import utime
import struct

#create an I2C object with mode I2C.CONTROLLER 
obj = I2C(1, I2C.CONTROLLER, baudrate = 100000)
print(obj.scan())                   # Check for devices on the bus
obj.mem_write('\x0C', 0x28, 0x3D)   # Send a 7 to sensor at 0x28, register 0x3D
utime.sleep(1)

#create the two byte arrays where the bytes read from the device will be stored 
b1 = bytearray(2)
b2 = bytearray(2)
b3 = bytearray(2)

while True:

    #read the bytes from the device at hex address 28, and from register addresses 1A-1F
    obj.mem_read(b1, 0x28, 0x1A)
    obj.mem_read(b2, 0x28, 0x1C)
    obj.mem_read(b3, 0x28, 0x1E)

    #unpack the 2 byte arrays using little endian into three short integers 
    ea1 = struct.unpack('<h',b1)
    ea2 = struct.unpack('<h',b2)
    ea3 = struct.unpack('<h',b3)

    #scaling 
    yaw = (ea1[0]/16)
    roll = (ea3[0]/16)
    pitch = (ea2[0]/16)

    #continously print the position of the 9 axis absolute orientation module 
    print("Yaw : " + str(yaw))
    print("Roll : " + str(roll))
    print("Pitch : " + str(pitch))

    utime.sleep(1)
