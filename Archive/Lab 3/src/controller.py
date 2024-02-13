"""! @file conroller.py
  The controller class file for our Lab 3 Motor Controller Assignment
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

#import relevant modules and files 
from motor_driver import MotorDriver
from encoder_reader import Encoder
import pyb
import utime

class P_Control(): 
    """! 
            This class  ... 
            """
    
    def __init__(self, in_Kp, in_setpoint, enapin, timer, enp1, mp1, mp2, coderp1, coderp2, codertimer):
        """!
        The initialization function inside the P_Control class ... 
        """
        
        #initialize values for setpoint, gain
        self.setpoint = in_setpoint
        self.Kp = in_Kp

        self.times = []
        self.position = []
        
        #create encoder object 
        self.enco1 = Encoder(coderp1, coderp2, codertimer)
        
        #initialize variables for motor driver 
        self.in1_pin = 0
        self.in2_pin = 0

        #create motor driver object 
        self.moe = MotorDriver(enapin, self.in1_pin, self.in2_pin, timer, enp1, mp1, mp2)

       

    def run(self,in_setpoint, z_ticks):
        """!
            The run function in the P_Control class...
            """  
        self.setpoint = in_setpoint 
        encout = self.enco1.read()
        self.times.append(utime.ticks_diff(utime.ticks_ms(), z_ticks))
        self.position.append(encout)
        PWM = self.Kp * (self.setpoint - encout) 
        if PWM > 100:
            PWM = 100
        elif PWM < -100:
            PWM = -100   
        self.moe.set_duty_cycle(PWM)
        return(PWM)
        
    def set_setpoint(self,in_sp):
        """!
            The set_setpoint function in the P_Control class...
            """
        
        self.setpoint = in_sp

    def set_Kp(self,des_Kp): 
        """!
            The set_Kp function in the P_Control class...
            """
        self.Kp = des_Kp 

    def zero(self):
        self.enco1.zero()

    def print_res(self):
        """!
            Print the step response data
            """
        for i in range(len(self.times)):
            print(str(self.times[i]) + "," + str(self.position[i]))