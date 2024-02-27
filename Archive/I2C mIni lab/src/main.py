"""! @file bno_test.py
  
  This file 
  
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

from pyb import I2C
from pyb import Pin
import utime
import struct

obj = I2C(1, I2C.CONTROLLER, baudrate = 100000)
print(obj.scan())                   # Check for devices on the bus
obj.mem_write('\x0C', 0x28, 0x3D)   # Send a 7 to sensor at 0x28, register 0x3D
utime.sleep(1)

# Create byte arrays of size two to store the Euler angles into
b1 = bytearray(2)
b2 = bytearray(2)
b3 = bytearray(2)


# Read the Euler angles from the registers 1A through 1F
while True:
    # Talk to the device at address 0x28 and read the registers 
    # and store those values into the byte arrays
    obj.mem_read(b1, 0x28, 0x1A)
    obj.mem_read(b2, 0x28, 0x1C)
    obj.mem_read(b3, 0x28, 0x1E)

    ea1 = struct.unpack('<h',b1)
    ea2 = struct.unpack('<h',b2)
    ea3 = struct.unpack('<h',b3)
    yaw = (ea1[0]/16)
    roll = (ea3[0]/16)
    pitch = (ea2[0]/16)
    print("Yaw : " + str(yaw))
    print("Roll : " + str(roll))
    print("Pitch : " + str(pitch))
    utime.sleep(1)
