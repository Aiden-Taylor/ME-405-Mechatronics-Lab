"""! @file encoder_reader.py
  
  The main file for our Lab 2 Read Motor Encoder Assignment. This file is used to read the position
  of a motor using the attatched motor encoder. This is accomplished by creating an Encoder class
  with several functions defined to aid in the task of reading the encoder including init, read, zero
  and loop. At the bottom of the code, the Encoder class is implemented and continuously prints the
  updated motor positions for two motors.
  
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

#import relevant modules 
import pyb 
import micropython
import time
micropython.alloc_emergency_exception_buf(100)

class Encoder:
    """! 
        This class implements encoders for an ME405 kit. 
        """

    def __init__(self, pin1, pin2, timer):
        """!
        The initialization function inside the Encoder class sets up the pins for timer channels, 
        the timer, and the two channels needed to read AB encoder quadrature output. 
        """
        #put some stuff here

        # pin1 and pin2 inputs should be in this format: pyb.Pin.board.PB7
        self.p1 = pyb.Pin(pin1, mode=pyb.Pin.IN)
        self.p2 = pyb.Pin(pin2, mode=pyb.Pin.IN)
        
        #initialize the timer with a prescaler of 0 and period of 65535 (maximum integer for 16 bit nuber)
        self.tim = pyb.Timer(timer, prescaler=0, period=65535)

        self.motor_position = 0
        self.curr_pos = 0
        self.prev_pos = 0
        self.delt = 0

        #prescaler: number of encoder ticks before timer count updates

        #setup channels 1 and 2 for the timer
        self.ch1 = self.tim.channel(1, mode=pyb.Timer.ENC_AB, pin=pin1)
        self.ch2 = self.tim.channel(2, mode=pyb.Timer.ENC_AB, pin=pin2)

    def readtim(self):
        """!
        The readtim function in the Encoder class returns the current timer counter value.
        """
        return(self.tim.counter())
    
    def read(self):
       """!
        The read function in the Encoder class calculates the correct delta in motor postition in degrees from the timer counter and adds 
        it to the current count.
        """
        #256*4*16 encoder ticks per rotation
        #256 slits
        #4 edges per slit
        #16 for gear ratio
        
        self.curr_pos = self.readtim()*360/(256*4*16)
        self.delt = self.curr_pos-self.prev_pos
        if self.delt >= 1000:
            self.delt -= 1440
        elif self.delt <= -1000:
            self.delt += 1440
        self.motor_position += self.delt
        return(self.motor_position)

    def zero(self):
        """!
        The zero function in the Encoder class sets the timer count, motor position, prev_pos, curr_pos, and delt to zero.
        This can be used to initialize the position of the motor. 
        """
        #set the counter to zero
        self.motor_position = 0
        self.prev_pos = 0
        self.curr_pos = 0
        self.delt = 0
        self.tim.counter(0)

if __name__ == "__main__": #only runs if its the main program 
    #put a main test prog here
    enc1 = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    enc2 = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    while True:
        enc1.prev_pos = enc1.curr_pos
        enc2.prev_pos = enc2.curr_pos
        time.sleep(0.1)

        print("Motor 1: " + str(enc1.loop()) + " degrees")
        print("Motor 2: " + str(enc2.loop()) + " degrees")
   