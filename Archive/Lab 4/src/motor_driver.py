"""! @file motor_driver.py
  
  This file is responsible for implementing the speed control for a motor using a PWM signal that 
  can be modified based on the users input. This file can be used on multiple motors in a main 
  file at the same time as it takes the motor pins as an input. 

  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  
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
        @param en_pin The value sent to the enable pin controlled by the microcontroller. When the en_pin
               is set high, it enables the motor. 
        @param in1pwm The initial pwm percentage value sent to the timer 
               channel corresponding to the first motor pin. When in1pwm 
               is set to 0, the motor runs in the forward direction.  
        
        @param in2pwm The initial pwm percentage value sent to the timer 
               channel corresponding to the second motor pin. When in2pwm 
               is set to 0, the motor runs in the reverse direction. 
        
        @param timer The timer channel that corresponds with the motor pins 
               used for the motor. 
        
        @param enapin The chosen enable pin number controlled by the microcontroller corresponding 
               to EN_A/OCD_A or EN_B/OCD_B on the L6206. 
        
        @param motorpin1 The first chosen motor pin on the CPU corresponding to the IN1 A/B pin 
               on the L6206.
        
        @param motorpin2 The second chosen motor pin on the CPU corresponding to the IN2_A/B pin 
               on the L6206.
        
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