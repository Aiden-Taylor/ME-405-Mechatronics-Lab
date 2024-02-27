"""! @file main.py
  The main file for our Lab 3 Motor Controller Assignment. This file creates a 
  P_controller class object and runs a loop to test several Kp values to find the ideal 
  Kp value for motor control. 


  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

import controller
import pyb
import utime

#motor init
ena = pyb.Pin.board.PC1
in1 = pyb.Pin.board.PA0
in2 = pyb.Pin.board.PA1
motimer = 5

#encoder init
cp1 = pyb.Pin.board.PC6
cp2 = pyb.Pin.board.PC7
cptimer = 8
Kp_init = 1
setp_init = 16384

#establish controller class
var = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

#init step_test to be true
step_test = True 

#loop to run multiple Kp values for one rotation each 
while step_test:
    
    #runs the controller, running closed-loop step response tests 
    #in which the setpoint is changed so as to rotate the motor by about 
    #one revolution and stop it at the final position.
    #Note:16,384 encoder ticks per revolution

    #Kp_init = float(input("Input a Kp: "))
    Kp_init = 0.05

    #zero the encoder count and position
    var.zero()
    var.set_Kp(Kp_init)
    setp_in = 16384
    running = True
    timtimeint = utime.ticks_ms()

    # Run the motor for 2 seconds
    for n in range(200):
        
        var.run(setp_in, timtimeint)
        utime.sleep_ms(10)

    var.moe.set_duty_cycle(0)
    var.print_res()

    if input('run another step test? y/n') != 'y':
        step_test = False 
