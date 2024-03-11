import pyb
import utime

##----- init

power = False


#part 16
#a)
#ii)
obj = pyb.I2C(1, pyb.I2C.CONTROLLER, baudrate = 100000)

#iii)
pinPF0 = pyb.Pin(pyb.Pin.Board.PF0, pyb.Pin.I2C2_SDA)
pinPF1 = pyb.Pin(pyb.Pin.Board.PF1, pyb.Pin.I2C2_SCL)

#b)
###----- off state
#assume we set addres to hex 2

#set the I/O Direction Register
obj.mem_write('\xFF', 0x02, 0x00)

#disable internal Pull-Up resistor
obj.mem_write('\x00', 0x02, 0x06)

#disable all leds
obj.mem_write('\xFF', 0x02, 0x09)

##------ toggle power state

power = ~power
if power:
    for i in range(3):
        #enable all leds
        obj.mem_write('\x00', 0x28, 0x09)
        utime.sleep(0.25)

        #disable all leds
        obj.mem_write('\xFF', 0x28, 0x09)
        utime.sleep(0.25)

##------ state of charge state
