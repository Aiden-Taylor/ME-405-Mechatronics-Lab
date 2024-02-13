"""! @file motor_driver.py
  The main file for our week 4 Lab 2
  """

#import relevant modules 

import pyb 
import micropython

micropython.alloc_emergency_exception_buf(100)

class MotorDriver:
    """! 
      This class implements a motor driver for an ME405 kit. 
      """

    def __init__ (self, en_pin, in1pwm, in2pwm, timer, enapin, motorpin1, motorpin2):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several parameters)
        """

        #set pin as an output for ENA/OCD and set as open-drain outputs with pullup resistors enabled
        self.ena_pin = pyb.Pin((enapin), pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
        self.ena_pin.value(en_pin)

        #set pin as an output for IN1A
        self.m_pin1 = pyb.Pin((motorpin1), pyb.Pin.OUT_PP)

        #set pin as an output for IN2A
        self.m_pin2 = pyb.Pin((motorpin2), pyb.Pin.OUT_PP) 

        #create timer on channel 1 to work with pin for PWM for the motor
        self.tim = pyb.Timer(timer, freq=20000)
        self.ch1 = self.tim.channel(1, pyb.Timer.PWM, pin=self.m_pin1)
        self.ch1.pulse_width_percent(in1pwm)

        #create timer on channel 2 to work with pin for PWM for the motor
        self.ch2 = self.tim.channel(2, pyb.Timer.PWM, pin=self.m_pin2)
        self.ch2.pulse_width_percent(in2pwm)

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
        
        self.ena_pin.value(1) #sets the enable pin high 

        if level > 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level)
            
        else:
            level = level*-1
            self.ch2.pulse_width_percent(0)
            self.ch1.pulse_width_percent(level)
            
             
        print(f"Setting duty cycle to {level}")
    
if __name__ == "__main__":
    # Script code goes here
    enpin = 0
    a_pin = 0
    another_pin = 0
    a_timer = 3
    enp1 = pyb.Pin.board.PC1
    mp2 = pyb.Pin.board.PA0
    mp3 = pyb.Pin.board.PA1
    moe = MotorDriver(enpin, a_pin, another_pin, a_timer, enp1, mp2, mp3)
    while True:
        moe.set_duty_cycle(int(input('set a duty cycle')))
        # moe.set_duty_cycle(0)