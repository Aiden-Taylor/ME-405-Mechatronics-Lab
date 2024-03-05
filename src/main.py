"""!
@file main.py

    This is the main file for the term project. 

@author Aiden Taylor, Jack Foxcroft, Julia Fay
@date   2024-Mar-04 

"""

#import all relevant modlues and files 
import gc
import pyb
import cotask
import task_share
import controller
import utime
import mlx_cam
import csv_reader

#Initialize shared variables between tasks. 
stp = 0
sht = False 


def task1_fun(data):
    """!
    Task which runs the panning motion for motor #1. 
    @param 
    """
    setpoint, shoot = data
    t1_state = 0; 
    
    while True:
        # Implement FSM inside while loop
        
        #S0 - MOTOR INIT 
        #Initialize motor pins, Kp value, and position 
        if (t1_state == 0):
            # Run state zero code
            print("The state is ", t1_state)
            ena = pyb.Pin.board.PC1
            in1 = pyb.Pin.board.PA0
            in2 = pyb.Pin.board.PA1
            motimer = 5

            #encoder init
            cp1 = pyb.Pin.board.PC6
            cp2 = pyb.Pin.board.PC7
            cptimer = 8
            Kp_init = 0.05
            setpoint = 16384
            setp_init = 0       #   FIGURE OUT WHAT TO SET THIS TO FOR EACH MOTOR

            #establish controller object
            global var
            var = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

            #zero the encoder count and position
            var.zero()
            var.set_Kp(Kp_init)
            timtimeint = utime.ticks_ms()
            
            var.moe.set_duty_cycle(0)
                    
            t1_state = 1
        
        #S1 - MOVE     
        elif (t1_state == 1):
            # Run state one code
            print("The state is ", t1_state)
               
            var.run(setpoint, timtimeint)
            
            if shoot == True: 
                t1_state = 2
            
        #S2 - IDLE TO SHOOT     
        elif (t1_state == 2):
            # Run state two code
            print("The state is ", t1_state)
            var.moe.set_duty_cycle(0)
    
        else:
            # If the state isnt 0, 1, or 2 we have an
            # invalid state
            raise ValueError('Invalid state')
            
        yield t1_state
    
    
    #want target to be at zero (want the controller to force something to zero)

def task2_fun(data):
    """!
    Task which deals with the thermal camera. 
    @param 
    """
    t2_state = 0
    setpoint, shoot = data
    
    
    while True:
        # Implement FSM inside while loop
        
        #S0 - CAMERA INIT 
        if t2_state == 0:
            
            #Initialize camera object 
            i2c_bus = mlx_cam.I2C(1)

            print("MXL90640 Easy(ish) Driver Test")

            # Select MLX90640 camera I2C address, normally 0x33, and check the bus
            i2c_address = 0x33
            scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
            print(f"I2C Scan: {scanhex}")

            # Create the camera object and set it up in default mode
            camera = mlx_cam.MLX_Cam(i2c_bus)
            
            t2_state = 1

            ##------------TEMPORARY-----------------
            setpoint = 16384
            shoot = False
        
        #S1 - GET CURRENT IMAGE     
        elif t2_state == 1: 
            
            try:
                # Get and image and see how long it takes to grab that image
                print("Click.", end='')
                begintime = utime.ticks_ms()
                var.zero()
                image = camera.get_image()
                #print(f" {utime.ticks_diff(utime.ticks_ms(), begintime)} ms")
                t2_state = 2 
            except KeyboardInterrupt:
                break
            
        #S2 - INTERPRET IMAGE 
        elif t2_state == 2: 
            
            reed = csv_reader.CSV(camera.get_csv(image.v_ir, limits=(0, 99)))
            reed.readdata()
            col, total = reed.col_largest()
            print(col,total)
    
            t2_state = 3       
            
        #S3 - CALCULATE NEW SETPOINT 
        elif t2_state == 3: 
            done = False
            # FOV = 55 degrees x 35 degrees
            
            # Gear Ratio = 6:1
            # Our motors current position is the center of the frame, so column 16 
            # If we want to make the col with the highest total heat value the new center of the frame 
            # Then we have to calculate how many encoder ticks it takes to reach that position 
            
            #calculate how many degrees we need to move the turret
            # 1 pixel = 1.72 degrees
            # Resolution = 32 x 24 pixels
            degs = (col-16)*1.72

            #calculate how many encoder ticks it takes to move that distance
            # Divide by 360 to get rid of degrees, multiply by 16384 to convert to encoder ticks, multiply 
            # by 6 
            setpoint = int(degs * 16384 / 360 * 6)
            
            if setpoint == 0: 
                shoot = True
                t2_state = 4 
            
        #S4 - IDLE FOR SHOOT  
        elif t2_state == 4: 

                if shoot == False: 
                    t2_state = 1
            
        yield t2_state
            
def task3_fun(shoot):
    """!
    Task which runs the trigger motion for motor #2. 
    @param 
    """
    t3_state = 0; 

    while True:
        # Implement FSM inside while loop
        
        #S0 - MOTOR INIT 
        #Initialize motor pins, Kp value, and position 
        if (t3_state == 0):
            ena = pyb.Pin.board.PA10
            in1 = pyb.Pin.board.PB4
            in2 = pyb.Pin.board.PB5
            motimer = 3

            #encoder init
            cp1 = pyb.Pin.board.PB6
            cp2 = pyb.Pin.board.PB7
            cptimer = 4
            trigger_Kp_init = 0.05
            setp_init = 16384

            #establish controller class
            var2 = controller.P_Control(trigger_Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

            #set the Kp value 
            Kp_init = 0.05
            
            #zero the encoder count and position
            var2.zero()
            var2.set_Kp(Kp_init)
            timtimeint = utime.ticks_ms()

            #start the motor off as unmoving 
            var2.moe.set_duty_cycle(0)
            
            #always go to state 1 
            t3_state = 1 
            
        #S1 - WAIT 
        elif (t3_state == 1):
            
            var2.moe.set_duty_cycle(0)
            
            if shoot == True: 
                t3_state = 2 
                
        #S2 - SHOOT 
        elif (t3_state == 2): 
            
            #CHANGE THIS VALUE 
            trigger_sp = 16384  
            var2.run(trigger_sp, timtimeint)
            if var2.run(trigger_sp, timtimeint) < 5: 
                t3_state = 1
            
               
        else:
            # If the state isnt 0, 1, or 2 we have an
            # invalid state
            raise ValueError('Invalid state')
            
        yield t3_state  
           


#-------------------------------------------------------------------------------------------------------  

if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")
 
    # Create a share and a queue to test function and diagnostic printouts
    stp = task_share.Share('h', thread_protect=False, name="Shared Setpoint")
    sht = task_share.Share('h', thread_protect=False, name="Shared Shoot")
    

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    #paning motor task
    task1 = cotask.Task(task1_fun, name="Task_1", priority=2, period=10,
                        profile=True, trace=False, shares=(stp, sht))
    
    #camera task
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=10,
                        profile=True, trace=False, shares=(stp, sht))
    
    #trigger motor task 
    task3 = cotask.Task(task3_fun, name="Task_3", priority=2, period=10,
                       profile=True, trace=False, shares=(stp, sht))
    
    #put all of the tasks on the task list 
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)


    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    t0 = utime.ticks_ms()
    while True:
        try:
            cotask.task_list.pri_sched()
            if (utime.ticks_ms()-t0) > 1000:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    #print('\n' + str (cotask.task_list))
    #print(task_share.show_all())
    #print(task1.get_trace())
    #print('')
    #var.print_res()
    #var2.print_res()