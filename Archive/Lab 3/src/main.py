"""! @file main.py
  The main file for our Lab 3 Motor Controller Assignment
  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  """

import controller
#from step_GUI import Step_GUI
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



var.zero() 

#var.run(setp_init)

step_test = True 

while step_test:
    
    # which runs the controller, running closed-loop step response tests 
        #in which the setpoint is changed so as to rotate the motor by about 
        #one revolution and stop it at the final position.
    
    # 16,384 encoder ticks per revolution
    cnt = 0
    Kp_init = float(input("Input a Kp: "))
    var.set_Kp(Kp_init)
    setp_in = 16384
    running = True
    timtimeint = utime.ticks_ms()
    while running:
        if var.run(setp_in, timtimeint) < 2:
            cnt += 1
            
        else:
            cnt = 0
        
        if cnt >= 5:
            running = False
            var.moe.set_duty_cycle(0)

        utime.sleep_ms(10)

    var.zero()
    var.print_res()

    if input('run another step test? y/n') != 'y':
        step_test = False 
