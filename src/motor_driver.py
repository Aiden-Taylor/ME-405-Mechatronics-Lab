"""! @file main.py
  The main file for our week 4 Lab 2
  """

#import relevant modules 

import pyb 
import cqueue
import micropython
import time

micropython.alloc_emergency_exception_buf(100)

class MotorDriver:
    """! 
      This class implements a motor driver for an ME405 kit. 
      """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several parameters)
        """
    
        #set pin PA10 as an output for ENA/OCD and set as open-drain outputs with pullup resistors enabled
        global pinA10
        pinA10 = pyb.Pin((pyb.Pin.board.PA10), pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
        pinA10.value(en_pin)

        #set pin PB4 as an output for IN1A
        pinB4 = pyb.Pin((pyb.Pin.board.PB4), pyb.Pin.OUT_PP)

        #set pin PB5 as an output for IN2A
        pinB5 = pyb.Pin((pyb.Pin.board.PB5), pyb.Pin.OUT_PP) 

        #create timer 3 on channel 2 to work with pin PB4 for PWM for the motor
        tim3 = pyb.Timer(timer, freq=20000)
        global ch1
        ch1 = tim3.channel(1, pyb.Timer.PWM, pin=pinB4)
        ch1.pulse_width_percent(in1pin)

        #create timer 3 on channel 2 to work with pin PB5 for PWM for the motor
        tim3 = pyb.Timer(timer, freq=20000)
        global ch2
        ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pinB5)
        ch2.pulse_width_percent(in2pin)

        print ("Creating a motor driver")


    def set_duty_cycle(self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        
        pinA10.value(1) #sets the enable pin high 

        if level > 0:
            ch1.pulse_width_percent(0)
            ch2.pulse_width_percent(level)
            
        else:
            level = level*-1
            ch2.pulse_width_percent(0)
            ch1.pulse_width_percent(level)
            
             
        print(f"Setting duty cycle to {level}")
    
if __name__ == "__main__":
    # Script code goes here
    enpin = 0
    a_pin = 0
    another_pin = 0
    a_timer = 3
    moe = MotorDriver(enpin, a_pin, another_pin, a_timer)
    while True:
        moe.set_duty_cycle(int(input('set a duty cycle')))
        # moe.set_duty_cycle(0)