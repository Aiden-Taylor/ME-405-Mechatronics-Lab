"""! @file conroller.py
  The main file for our Lab 3 Motor Controller Assignment
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

#import relevant modules and files 
import motor_driver
import read_encoder

class P_Control(): 
    """! 
            This class  ... 
            """
    
    def __init__(self,setpoint,Kp):
        """!
        The initialization function inside the P_Control class ... 
        """
        self.setpoint = setpoint 
        self.Kp = Kp 


    def run(self,setpoint,output):
        """!
            The run function in the P_Control class...
            """        

    def set_setpoint(self,des_setpoint):
        """!
            The set_setpoint function in the P_Control class...
            """
        
        self.Kp = des_setpoint

    def set_Kp(self,des_Kp): 
        """!
            The set_Kp function in the P_Control class...
            """
        self.Kp = des_Kp 