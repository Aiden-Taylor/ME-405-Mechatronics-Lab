"""!
@file main.py

    This is the main file for the term project. 

@author Aiden Taylor, Jack Foxcroft, Julia Fay
@date   2024-Mar-04 

note: the encoder reader file was changed and doxygen comments there need to be updated 

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

#create global variable done 
done = False 

def task1_fun(data):
    """!
    Task which runs the panning motion for motor #1. 
    @param 
    """
    setpoint_share, shoot_share = data  # Access shared variables from data tuple
    t1_state = 0; 
    
    print("Starting task 1")
    
    while True:
        
        # Implement FSM inside while loop
        #S0 - MOTOR INIT 
        #Initialize motor pins, Kp value, and position 
        if (t1_state == 0):
            # Run state zero code
            print("Task 1 state: ", t1_state)
            print("Initializing panning motor and encoder")
            utime.sleep(2)
            ena = pyb.Pin.board.PC1
            in1 = pyb.Pin.board.PA0
            in2 = pyb.Pin.board.PA1
            motimer = 5

            #encoder init
            cp1 = pyb.Pin.board.PC6
            cp2 = pyb.Pin.board.PC7
            cptimer = 8
            Kp_init = 0.05
            setpoint = 0
            setp_init = 0       #   FIGURE OUT WHAT TO SET THIS TO FOR EACH MOTOR

            #establish controller object
            global var
            var = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

            #zero the encoder count and position
            var.zero()
            var.set_Kp(Kp_init)
            timtimeint = utime.ticks_ms()
            var.moe.set_duty_cycle(0)

            #always go to state 1 from init  
            t1_state = 1   


        #S1 - GET INTO POSITION     
        elif (t1_state == 1):
            
            #create the 180 degree setpoint (16384 encoder counts per rev, w/ a gear ratio of 6:1 we need 3*
            one_eighty = 3*16384
            #get current clock count 
            timtimeint = utime.ticks_ms()
            var.run(one_eighty,timtimeint)
            print("Task 1 state: ", t1_state)
            if abs(var.get_PWM()) < 10:
                #turn off trigger motor 
                print("I moved 180!")
                var.moe.set_duty_cycle(0) 
                #utime.sleep(2)
                t1_state = 2
                var.zero()
        
        #S2 - MOVE     
        elif (t1_state == 2):
            
            #im thinking we need to add one more shared variable so we can give the panning 
            #motor some time to reach its new setpoint before it starts going to a new setpoint 
            #like we hold off on getting a new image and recalculating a new setpoint until 
            #the panning motor has reached within a certain value of its last setpoint 
            
            #get the setpoint from the share
            setpoint = setpoint_share.get()  # Get setpoint from shared variable
            print("Task 1 state: ", t1_state)
            print(f"updating motor setpoint to: {setpoint}")
            #update the motors setpoint 
            var.run(setpoint, timtimeint)
           
            shoot = shoot_share.get()  # Get shoot flag from shared variable
              
            if shoot == True: 
                print("Time to shoot")
                t1_state = 3
            
        #S3 - IDLE TO SHOOT     
        elif (t1_state == 3):
            print("Task 1 state: ", t1_state)
            print("Panning motor idling to shoot")
            #set duty cycle to 0 to stop the motor 
            var.moe.set_duty_cycle(0)
            #if the trigger has shot its shot, return back to state 2 
            if shoot == False: 
                t1_state = 2
    
        else:
            # If the state isnt 0, 1, 2, or 3 we have an
            # invalid state
            raise ValueError('Invalid state')
            
        print("Exiting task 1")
        yield 0
    
    
    #want target to be at zero (want the controller to force something to zero)

def task2_fun(data):
    """!
    Task which deals with the thermal camera. 
    @param 
    """
    t2_state = 0
    setpoint_share, shoot_share = data  # Access shared variables from data tuple
    print("Starting task 2")
       
    while True:

        # Implement FSM inside while loop
        #S0 - CAMERA INIT 
        if t2_state == 0:
            print("Task 2 state: ", t2_state)
            print("Initializing thermal camera")
            #utime.sleep(2)
            #Initialize camera object 
            i2c_bus = mlx_cam.I2C(1)

            #print("MXL90640 Easy(ish) Driver Test")

            # Select MLX90640 camera I2C address, normally 0x33, and check the bus
            i2c_address = 0x33
            scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
            #print(f"I2C Scan: {scanhex}")

            # Create the camera object and set it up in default mode
            gc.collect()
            camera = mlx_cam.MLX_Cam(i2c_bus)
            print(f"Current refresh rate: {camera._camera.refresh_rate}")
            camera._camera.refresh_rate = 10.0
            print(f"Refresh rate is now:  {camera._camera.refresh_rate}")
            utime.sleep(2)
            image = None
            gc.collect()
            
            t2_state = 1
            setpoint = 0
            shoot = False
        
        #S1 - GET CURRENT IMAGE     
        elif t2_state == 1: 
            print("Task 2 state: ", t2_state)
            print("Getting current image")
            #utime.sleep(2)
            try:
                # Get and image and see how long it takes to grab that image
                print("Click.", end='')
                begintime = utime.ticks_ms()
                var.zero()
                #while not image:
                #    image = camera.get_image_nonblocking()
                #    yield t2_state
                image = camera.get_image()
                t2_state = 2
                
            except KeyboardInterrupt:
                break
            
        #S2 - INTERPRET IMAGE 
        elif t2_state == 2: 
            print("Task 2 state: ", t2_state)
            print("Interpreting image")
            #utime.sleep(2)
            reed = csv_reader.CSV(camera.get_csv(image, limits=(0, 99)))
            reed.readdata()
            col, total = reed.col_largest()
            print("COLLUMN", col,"TOTAL", total)
    
            t2_state = 3       
            
        #S3 - CALCULATE NEW SETPOINT 
        elif t2_state == 3: 
            print("Task 2 state: ", t2_state)
            print("Calculating new setpoint")
            #utime.sleep(2)
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
            # by 6 to account for the gear ratio 
            new_setpoint = int((degs/360) * 16384 * 6)
            print("The new setpoint is", new_setpoint)
            #update the shares value 
            setpoint_share.put(new_setpoint)
            print(setpoint_share)
            
            #default to going back to state 1 to get an image
            t2_state = 1
            
            #if the new setpoint is 0 then its time to shoot 
            if new_setpoint == 0: 
                print("Time to shoot!")
                shoot = True
                shoot_share.put(shoot)
                t2_state = 4 
            
            #if its not time to shoot, keep putting shoot = False into the queue 
            shoot_share.put(shoot)
        #S4 - IDLE FOR SHOOT  
        elif t2_state == 4: 
            print("Task 2 state: ", t2_state)
            print("Camera Idling to shoot")
            #utime.sleep(2)
            if shoot == False: 
                t2_state = 1
        print("Exiting task 2")    
        yield 0
            
def task3_fun(data):
    """!
    Task which runs the trigger motion for motor #2. 
    @param 
    """
    t3_state = 0; 
    print("Task 3")
    
    setpoint_share, shoot_share = data  # Access shared variables from data tuple

    while True:
        
        # Implement FSM inside while loop
        #S0 - MOTOR INIT 
        #Initialize motor pins, Kp value, and position 
        if (t3_state == 0):
            print("Task 3 state: ", t3_state)
            print("Initializing trigger motor and encoder")
            #utime.sleep(2)
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
            print("Task 3 state: ", t3_state)
            print("Trigger motor waiting to shoot")
            #utime.sleep(2)
            var2.moe.set_duty_cycle(0)
            
            shoot = shoot_share.get()  # Get shoot flag from shared variable
            
            if shoot == True: 
                t3_state = 2 
                shoot_share.put(shoot) # Put shoot back in so that Task 1 can get it 
                
            shoot_share.put(shoot) # Put shoot back in so that Task 1 can get it 
                
        #S2 - SHOOT 
        elif (t3_state == 2): 
            print("Task 3 state: ", t3_state)
            print("Time to shoot!")
            
            #create the setpoint such that the trigger moves the corrent distance 
            #estimate to be half a revolution   
            trigger_sp = 16384/2   
            #get current clock count 
            timtimeint = utime.ticks_ms()
            #run the motor 
            var2.run(trigger_sp, timtimeint)
            #if the motor has a low PWM value, assume it has reached its position 
            if abs(var2.get_PWM()) < 10: 
                #turn off trigger motor 
                var2.moe.set_duty_cycle(0)
                t3_state = 1
                shoot = False 
                shoot_share.put(shoot)
                done = True
            
               
        else:
            # If the state isnt 0, 1, or 2 we have an
            # invalid state
            raise ValueError('Invalid state')
        
        print("Exiting task 3")      
        yield 0
          
           


#-------------------------------------------------------------------------------------------------------  

if __name__ == "__main__":
    #print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          #"Press Ctrl-C to stop and show diagnostics.")
    
 
    # Create a share and a queue to test function and diagnostic printouts
    print("Creating shared queues")
    stp = task_share.Share('h', thread_protect=False, name="Shared Setpoint")
    sht = task_share.Share('h', thread_protect=False, name="Shared Shoot")
    #done = '_____'
    

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    print("Creating task list")
    #paning motor task
    task1 = cotask.Task(task1_fun, name="Task_1", priority=2, period=10,
                        profile=True, trace=False, shares=(stp, sht))
    
    #camera task
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=100,
                        profile=True, trace=False, shares=(stp, sht))
    
    #trigger motor task 
    task3 = cotask.Task(task3_fun, name="Task_3", priority=2, period=100,
                       profile=True, trace=False, shares=(stp, sht, ))
    
    #put all of the tasks on the task list 
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)


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
            break
        

    # Print a table of task data and a table of shared information data
    #print('\n' + str (cotask.task_list))
    #print(task_share.show_all())
    #print(task1.get_trace())
    #print('')
    #var.print_res()
    #var2.print_res()