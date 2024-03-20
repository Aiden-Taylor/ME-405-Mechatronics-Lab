"""!
@mainpage Software Overview

@section intro_sec Introduction

This main page covers the workings of the main.py file used for this project, as well as the files that were used to make the whole system work.

@section file_sec Files

This is an overview of the files that we wrote and utilized:

@subsection controller_sec controller.py

This file is used as a high-level proportional controller for our motors. We use it to control the desired position of our motors, and also to interface with some of the lower-level files, seen below.

@subsection csv_sec csv_reader.py

This file was originally used for a plotter, but for the purposes of this project we adapted it to read the output of the thermal camera. We wrote a method in the class that reads the camera data, and then calculates the hottest thermal column, which is what we used to pick an aiming point.

@subsection encoder_sec encoder_reader.py

This file is a fairly self-explanatory class. We use it to read from the encoders and handle all the calculations related to determining the position of the motors. This file is referenced by the controller to read the motor positions.

@subsection mlx_sec mlx_cam.py

This is a file that was provided to us to read the infrared camera output. It was utilized in Task 2 of our main file.

@subsection motor_sec motor_driver.py

This file is used to control the speed of the motors. It takes a desired pwm output and feeds it to the motor driver. This file is also referenced by the controller, which uses this file and the encoder reader to create an effective proportional controller.

@section task_sec Tasks

@image html taskdiag.png

The following are the tasks and states used in the main file of this project:

@subsection t1_sec Task 1

@image html t1statediag.png

Task 1 runs the panning motion for motor #1. This task first moves the turret into the 
    aiming position (180 degrees from initial position). Then, updates the panning motor 
    setpoint calculated by the thermal camera and runs until the PWM signal falls below 50%
    for more than 20 cycles and sets the panning motor duty cycle to 0 and waits for the trigger
    motor to complete its task. These are the states that are utilized in Task 1:

@subsubsection t1s0_sec State 0

This state is an initialization state for the panning motor that sets up the enable, pwm, and encoder pins, as well as
    establishing the controller class instance for the pan.

@subsubsection t1s1_sec State 1

This state is used to capture an image. Once that is completed, we move to state 2.

@subsubsection t1s2_sec State 2

This state is used when the turret is panning to track the target. In this current implementation of our code, we are not actively tracking 
    a target, we are instead waiting for the 5 seconds and then turning towards the target and firing. If we wanted to implement active
    tracking in the future, this state is ready for that, with a few modifications.

@subsubsection t1s3_sec State 3

This state is an idle for the panning motor. This is used both when we are tracking the duel target, and when we are waiting for our turret to fire



@subsection t2_sec Task 2

@image html t2statediag.png

Task 2 deals with the thermal camera. It initializes the camera's i2c communication
    protocal them waits until the panning motor completes its initial movement to the aiming position
    180 degrees from the initial postion. Then wait 3.25 seconds and get the image.
    Then, using the csv_reader class, calculate the column with the maximum summed thermal
    signature and calculate the setpoint based on the column. These are the states that are utilized in Task 1:

@subsubsection t2s0_sec State 0

This state is an initialization state for the camera that intitializes the mlx_cam class instance, as well as setting the refresh rate of the camera.

@subsubsection t2s1_sec State 1

This state is used to spin the whole turret 180 degrees at the start of the duel. Once it has turned, it switches to state 3.

@subsubsection t2s2_sec State 2

This state utilizes the csv reader to interpret the data that was captured by the camera in state 1. This gives us a column from the data that we need to
    aim at. This moves us to state 3.

@subsubsection t2s3_sec State 3

This state takes the data that we got from the csv reader and uses trigonometry and information about our camera and setup geometry to calculate the angle 
    that our turret needs to turn to correctly aim at the target, and then it uses a shared variable to pass that information to Task 1 and 3.
    
@subsubsection t2s4_sec State 4

This state waits for the turret to fire and does not take any images that may cause lag.

@subsubsection t2s5_sec State 5

This state waits for the panning motor to spin 180 degrees at the start of the duel before taking any images.

    
@subsection t3_sec Task 3

@image html t3statediag.png

Task 3 runs the trigger motion for the motor #2. First, task 3 waits until the panning
    motor reaches the setpoint calculated by the thermal camera. Then, it runs the trigger motor
    to a setpoint of 30 degrees, then returns to its intial position. The states it uses are below:

@subsubsection t3s0_sec State 0

This state is an initialization state for the trigger motor that sets up the enable, pwm, and encoder pins, as well as
    establishing the controller class instance for the trigger.

@subsubsection t3s1_sec State 1

This state is used to wait until the turret is ready to fire

@subsubsection t3s2_sec State 2

This state is used when the turret is firing. This activates the trigger motor to pull until it reaches the desired setpoint that we 
    tested to guarantee that the turret fires.

@subsubsection t3s3_sec State 3

This state returns the trigger mechanism to its zero location after firing.

@subsection t4_sec Task 4

@image html t4statediag.png

Task 4 is a simple task that acts as our safety system. Our design used a safety wire that when pulled, shuts down the whole system. The states used are as follows:

@subsubsection t4s0_sec State 0

This state simple initializes the variables used for the safety wire.

@subsubsection t4s1_sec State 1

This state is where the safety task always operates after initialization. It checks that the wire is still connected. If the wire is pulled, then the system is halted and will no longer
    operate until it is reset and the safety wire is replaced.

@file main.py

This is the main file for the term project. 

@author Aiden Taylor, Jack Foxcroft, Julia Fay
@date   2024-Mar-18
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
import math

#create global variable done 
global done
done = False 

def task1_fun(data):
    """!
    Task 1 runs the panning motion for motor #1. This task first moves the turret into the 
    aiming position (180 degrees from initial position). Then, updates the panning motor 
    setpoint calculated by the thermal camera and runs until the PWM signal falls below 50%
    for more than 20 cycles and sets the panning motor duty cycle to 0 and waits for the trigger
    motor to complete its task
    
    @param data The tuple used to store all shared variables between tasks
    """
    setpoint_share, shoot_share, wait_share = data  # Access shared variables from data tuple
    t1_state = 0; 
    
    print("Starting task 1")
    
    while True:
        

        shoot = shoot_share.get()  # Get shoot flag from shared variable
        wait = wait_share.get()
        wait_share.put(wait)
        
        # Implement FSM inside while loop
        #S0 - MOTOR INIT 
        #Initialize motor pins, Kp value, and position 
        if (t1_state == 0):
            # Run state zero code
            print("Task 1 state: ", t1_state)
            print("Initializing panning motor and encoder")
            ena = pyb.Pin.board.PC1
            in1 = pyb.Pin.board.PA0
            in2 = pyb.Pin.board.PA1
            motimer = 5

            #encoder init
            cp1 = pyb.Pin.board.PC6
            cp2 = pyb.Pin.board.PC7
            cptimer = 8
            Kp_init = 10
            setpoint = 0
            setp_init = 0       #   FIGURE OUT WHAT TO SET THIS TO FOR EACH MOTOR
      

            #establish controller object
            global var
            var = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

            #zero the encoder count and position
            var.zero()
            var.set_Kp(Kp_init)
            global timtimeint
            timtimeint = utime.ticks_ms()
            var.moe.set_duty_cycle(0)
            #make sure the queue only has one value  
            wait_share.get()
            wait_share.put(True)
            count = 0

            #always go to state 1 from init  
            t1_state = 1   


        #S1 - GET INTO POSITION     
        elif (t1_state == 1):
            print("In the process of moving 180")
            #create the 180 degree setpoint (180 degrees, w/ a gear ratio of 6:1 so 6*180)
            one_eighty = 6*180
            var.run(one_eighty,timtimeint)
            print("Task 1 state: ", t1_state)
            
            #Check if the motor has reached this new position by checking if the PWM 
            #signal stays below 20 at least 10 times 
            if abs(var.get_PWM()) < 50:
                count += 1
            if count > 20: 
                print("I moved 180!")
                #turn off trigger motor
                var.moe.set_duty_cycle(0)
                #clear the queue and put False  
                wait_share.get()
                wait_share.put(False)
                #always go to the Idle state 3 to wait for the camera image to be taken 
                t1_state = 3
                #reset the count to zero 
                count = 0
                var.set_Kp(5)
                #zero the encoder position 
                var.zero()

        
        #S2 - TRACK TARGET    
        elif (t1_state == 2): 
            print("Task 1 state: ", t1_state)    
                    
            setpoint = setpoint_share.get()  # Get setpoint from shared variable
            setpoint_share.put(setpoint)     # Make sure the queue stays neutral
            print(f"updating setpoint is: {setpoint}")
           
            #update the motors setpoint and run 
            var.run(setpoint, timtimeint)
            
            #Check if the motor has reached this new position by checking if the PWM 
            #signal stays below 50 at least 20 times 
            if abs(var.get_PWM()) < 50:
                count += 1

            if count > 20:
                print("I moved to new setpoint!")
                #turn off trigger motor
                var.moe.set_duty_cycle(0)
                #clear the queue and put False  
                wait_share.get()
                wait_share.put(False)
                #go to the Idle state 3 to shoot 
                t1_state = 3
                #reset the count to zero 
                count = 0
                #zero the encoder position 
                var.zero()
                #tell the world its time to shoot 
                shoot_share.get()
                shoot_share.put(True)
    
            
        #S3 - IDLE     
        elif (t1_state == 3):
            print("Task 1 state: ", t1_state)
            print("Panning motor idling to shoot or take camera image")
            #set duty cycle to 0 to stop the motor 
            var.moe.set_duty_cycle(0)
            #if the trigger has shot its shot, return back to state 2 
            if wait == True: 
                t1_state = 2
                

        else:
            # If the state isnt 0, 1, 2, or 3 we have an
            # invalid state
            raise ValueError('Invalid state')
            
        print("Exiting task 1")
        yield 0


def task2_fun(data):
    """!
    Task 2 deals with the thermal camera. It initializes the camera's i2c communication
    protocal them waits until the panning motor completes its initial movement to the aiming position
    180 degrees from the initial postion. Then wait 3.25 seconds and get the image.
    Then, using the csv_reader class, calculate the column with the maximum summed thermal
    signature and calculate the setpoint based on the column.
    
    @param data The tuple used to store all shared variables between tasks
    """
    
    t2_state = 0
    setpoint_share, shoot_share, wait_share = data  # Access shared variables from data tuple
    print("Starting task 2")
       
    while True:
        # Implement FSM inside while loop
        
        #S0 - CAMERA INIT 
        if t2_state == 0:
            print("Task 2 state: ", t2_state)
            print("Initializing thermal camera") 
            #Initialize camera object 
            i2c_bus = mlx_cam.I2C(1)
            # Select MLX90640 camera I2C address, normally 0x33, and check the bus
            i2c_address = 0x33
            scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
            # Create the camera object and set it up in default mode
            gc.collect()
            camera = mlx_cam.MLX_Cam(i2c_bus)
            print(f"Current refresh rate: {camera._camera.refresh_rate}")
            camera._camera.refresh_rate = 10.0
            print(f"Refresh rate is now:  {camera._camera.refresh_rate}")
            image = None
            gc.collect()
            
            #always go to state 5 to wait for the panning motor to move 180 degrees 
            t2_state = 5      
            #initialize shoot to be false  
            shoot = False
        
        #S1 - GET CURRENT IMAGE     
        elif t2_state == 1: 
            print("Task 2 state: ", t2_state)
            print("Getting current image")
            print("Click.", end='')
            
            #zero the encoder to base the new setpoint calc off of the 
            #zeroed current position 
            var.zero()
            
            #init image to be none for the non blocking get image function 
            image = None
            begintime = utime.ticks_ms()
            utime.sleep(3.25)
            # Use non blocking code 
            while not image:
                image = camera.get_image()
                yield t2_state 
            print(f" {utime.ticks_diff(utime.ticks_ms(), begintime)} ms")
            
            #always go to state 2 to interpret image 
            t2_state = 2
            
        #S2 - INTERPRET IMAGE 
        elif t2_state == 2: 
            print("Task 2 state: ", t2_state)
            print("Interpreting image")
            #convert the image to CSV format 
            reed = csv_reader.CSV(camera.get_csv(image, limits=(0, 99)))
            #use the readdata() function to calculate the column with the highest 
            #thermal values 
            reed.readdata()
            #extract the column and total value and print 
            col, total = reed.col_largest()
            print("COLLUMN", col,"TOTAL", total)
            #always go to state 3 to calculate the new setpoint 
            t2_state = 3       
            
        #S3 - CALCULATE NEW SETPOINT 
        elif t2_state == 3: 
            print("Task 2 state: ", t2_state)
            print("Calculating new setpoint")
           
            # Camera FOV = 55 degrees x 35 degrees
            # Gear Ratio = 6:1
            # Our motors current position is the center of the frame, so column 16 
            # If we want to make the col with the highest total heat value the new center of the frame 
            # Then we have to calculate how many degrees it takes to reach that position 
            # 1 pixel = 1.72 degrees
            # Resolution = 32 x 24 pixels 
            #adjust for the trig of the table
            dist_from_table_edge = 4.5/12
            x = 8-dist_from_table_edge
            #trig_adjustment = math.atan(4.2/(8+x))/27.5 
            trig_adjustment = 0.5
            degs = (col-16)*1.72*trig_adjustment 
            #multiply degree value by 6 to account for the gear ratio and pring 
            new_setpoint = int(degs * 6)  
            print("The new setpoint is", new_setpoint)
            #update the shares values 
            setpoint_share.get()
            setpoint_share.put(new_setpoint)
            wait_share.get()
            wait_share.put(True)
            print("Updated the motor angle")
            shoot = False
            shoot_share.get()
            shoot_share.put(shoot)
            #always go to state 4 Idle for shoot since target has been found and new setpoint identified. 
            t2_state = 4 

        #S4 - IDLE FOR SHOOT  
        elif t2_state == 4: 
            print("Task 2 state: ", t2_state)
            print("Camera Idling to shoot")

        #S5 - WAIT FOR PANNING 
        elif (t2_state == 5):
            print('Waiting for panning motor to reach previous setpoint')
            #wait for it to spin to the current desired setpoint, and then transition to state 1
            wait = wait_share.get()
            wait_share.put(wait)
            if wait == False:
                t2_state = 1  
                
        else:
            # If the state isnt 0, 1, 2, 3, 4 or 5 we have an
            # invalid state
            raise ValueError('Invalid state')

        print("Exiting task 2")    
        yield 0
            
def task3_fun(data):
    """!
    Task 3 runs the trigger motion for the motor #2. First, task 3 waits until the panning
    motor reaches the setpoint calculated by the thermal camera. Then, it runs the trigger motor
    to a setpoint of 30 degrees, then returns to its intial position.

    @param data The tuple used to store all shared variables between tasks
    """
    t3_state = 0; 
    print("Task 3")
    
    setpoint_share, shoot_share, wait_share = data  # Access shared variables from data tuple

    while True:
        
        # Implement FSM inside while loop
        #S0 - MOTOR INIT  
        if (t3_state == 0):
            print("Task 3 state: ", t3_state)
            print("Initializing trigger motor and encoder")
            
            #Initialize motor pins, Kp value, and position
            ena = pyb.Pin.board.PA10
            in1 = pyb.Pin.board.PB4
            in2 = pyb.Pin.board.PB5
            motimer = 3

            #encoder init
            cp1 = pyb.Pin.board.PB6
            cp2 = pyb.Pin.board.PB7
            cptimer = 4
            trigger_Kp_init = 20
            setp_init = 360
            count2 = 0

            #establish controller class
            global var2
            var2 = controller.P_Control(trigger_Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

            #set the Kp value 
            Kp_init = 25
            
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
            print("Task 3 state: ", t3_state)
            print("Trigger motor waiting to shoot")
            var2.moe.set_duty_cycle(0)
            
            shoot = shoot_share.get()  # Get shoot flag from shared variable
            shoot_share.put(shoot)     # Put shoot back in so that Task 1 can get it
            #if shoot is true go to the shoot state 
            if shoot == True: 
                t3_state = 2 
                
        #S2 - SHOOT 
        elif (t3_state == 2): 
            print("Task 3 state: ", t3_state)
            print("Time to shoot!")
            
            #create the setpoint such that the trigger moves the corrent distance 
            #estimate to be 30 degrees  
            trigger_sp = 30   
            #run the motor 
            var2.run(trigger_sp, timtimeint)
            #if the motor has a low PWM value, assume it has reached its position 
            if var2.get_PWM() < 0: 
        
                #turn off trigger motor 
                var2.moe.set_duty_cycle(0)
                #always go to state 3 to return the trigger to its origonal posisiton 
                t3_state = 3
                #initialize count2 to be zero for the next state 
                count2 = 0
                #zero encoder count for the next state
                var2.zero()
                #set shoot to be False since we are done shooting 
                shoot = False 
                shoot_share.get()
                shoot_share.put(shoot)
                
        #S3 - RETURN TRIGGER MECHANISM
        elif (t3_state == 3): 
            print("Task 3 state: ", t3_state)
            print("Return Trigger")
            var2.set_Kp(2)
            #create the setpoint such that the trigger moves the corrent distance 
            #estimate to be half a revolution   
            trigger_sp = -30
            #get current clock count 
            #timtimeint = utime.ticks_ms()
            #run the motor 
            var2.run(trigger_sp, timtimeint)
            #if the motor has a low PWM value, assume it has reached its position 
            if abs(var2.get_PWM()) < 20: 
                count2 += 1
            if count2 > 15:
                #turn off trigger motor 
                var2.moe.set_duty_cycle(0)
                t3_state = 1
                global done
                done = True
 
        else:
            # If the state isnt 0, 1, 2 or 3 we have an
            # invalid state
            raise ValueError('Invalid state')
        
        print("Exiting task 3")      
        yield 0
          

def task4_fun(data):
    """!
    Task 4 enables a kill switch wire for the design to be terminated upon pulling 
    the wire. State 0 initializes the pin C0 to an input and if the pin it pulled
    terminate the program.
    
    @param data The tuple used to store all shared variables between tasks
    """
    t4_state = 0; 
    print("Task 4")
    while True:

        #S0 - INITALIZE PIN 
        if t4_state == 0:
            #initialize the input pin for the killswitch 
            safetypin = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN)
            #always go to state 1 
            t4_state = 1
            global safe
            safe = 0

        #S1 - SAFETY CHECK 
        elif t4_state == 1:
            #get the pin value 
            safe = safetypin.value()
            print("The safety is " + str(safe))
            #if the pin is not safe, terminate the program by setting done equal to True 
            if safe:
                global done
                done = True
                safe = True
                
        yield 0


#-------------------------------------------------------------------------------------------------------  

if __name__ == "__main__":
    #print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          #"Press Ctrl-C to stop and show diagnostics.")
    
 
    # Create a share and a queue to test function and diagnostic printouts
    print("Creating shared queues")
    stp = task_share.Share('h', thread_protect=False, name="Shared Setpoint")
    sht = task_share.Share('h', thread_protect=False, name="Shared Shoot")
    wait = task_share.Share('h', thread_protect=False, name="Shared Wait")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    print("Creating task list")
    #paning motor task
    task1 = cotask.Task(task1_fun, name="Task_1", priority=2, period=10,
                        profile=True, trace=False, shares=(stp, sht, wait))
    
    #camera task
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=180,
                        profile=True, trace=False, shares=(stp, sht, wait))
    
    #trigger motor task 
    task3 = cotask.Task(task3_fun, name="Task_3", priority=2, period=12,
                       profile=True, trace=False, shares=(stp, sht, wait))
    
    task4 = cotask.Task(task4_fun, name="Task_4", priority=2, period=12,
                       profile=True, trace=False, shares=(stp, sht, wait))
    
    #put all of the tasks on the task list 
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)


    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    print("Running the scheduler")
    t0 = utime.ticks_ms()
    while True:
        gc.collect()
        try:
            cotask.task_list.pri_sched()
            if (utime.ticks_ms()-t0) > 100000: #change this to be the hardware stop 
                raise KeyboardInterrupt
            elif done == True: 
                raise KeyboardInterrupt        
        
        except KeyboardInterrupt:
            var.moe.set_duty_cycle(0)
            var2.moe.set_duty_cycle(0)
            var.zero()
            utime.sleep(1)
            if not safe:
                for i in range(200):
                    var.run(-180*6, timtimeint)
                    utime.sleep_ms(10)
                var.moe.set_duty_cycle(0)
            break
        