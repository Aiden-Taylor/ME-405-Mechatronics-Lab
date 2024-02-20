"""! @file controller.py
  
  This file controls the speed of the motor by first comparing the actual position of the 
  motor and the desired position of the motor. This error value is multiplied by a constant
  Kp that is specified by the user. This calculation is then used to determine the PWM 
  signal that is sent to the motor. 
  
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
        The initialization function inside the P_Control class initializes all key parameters for this class. 
        This includes inputs for the motor pins and encoder pins used in the encoder_reader and motor_driver 
        imported classes. Additionally, the setpoint and Kp values are initialized, as well as the time and 
        position arrays that will be used within the P_control class. 
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
            The run function in the P_Control class calculates the PWM signal that will be 
            sent to the motor by taking into accound the setpoint of the motor, and 
            the current position of the motor. These values are subtracted to find the 
            error which is then multiplied by Kp. If this value exceeds -100 or 100, the 
            value is saturated to either -100 or 100. Then the set_duty_cycle function 
            imported from the motor_driver class is run. The calculated PWM signal is 
            returned at the end of the funciton. 
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
            The set_setpoint function in the P_Control class sets the setpoint of the motor 
            that will be used to calculate the error in the run fuction. 
            """
        
        self.setpoint = in_sp

    def set_Kp(self,des_Kp): 
        """!
            The set_Kp function in the P_Control class sets the Kp value that will be used to
            calculate the PWM value in the run function. 
            """
        self.Kp = des_Kp 

    def zero(self):
        """!
            The zero function in the P_Control class runs the zero function from the imported 
            encoder_reader class. This function sets the timer count, motor position, prev_pos, 
            curr_pos, and delt to zero. This can be used to initialize the position of the motor. 
            """
        self.enco1.zero()

    def print_res(self):
        """!
            The print_res fucntion in the P_Control class prints the position and time data 
            of the motor in a csv format that can be easily read and plotted in a separate funciton. 
            """
        for i in range(len(self.times)):
            print(str(self.times[i]) + "," + str(self.position[i]))
        self.times = []