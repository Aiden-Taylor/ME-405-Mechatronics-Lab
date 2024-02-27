"""!
@file main.py

    This is the main file for Lab 4, where we use the scheduler to cooperatively run our motor driver and another task.

@author Aiden Taylor, Jack Foxcroft, Julia Fay
@date   2024-Feb-20 Created from the provided example template

"""

import gc
import pyb
import cotask
import task_share
import controller
import utime

def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

    counter = 0
    while True:
        my_share.put(counter)
        my_queue.put(counter)
        counter += 1

        yield 0

def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares

    while True:
        # Show everything currently in the queue and the value in the share
        #print(f"Share: {the_share.get ()}, Queue: ", end='')
        while q0.any():
            print(f"{the_queue.get ()} ", end='')
        #print('')

        yield 0

def task3_fun():
    """!
    Task which runs the controller for motor #1. 
   
    """
    #loop to run multiple Kp values for one rotation each 
    
    #runs the controller, running closed-loop step response tests 
    #in which the setpoint is changed so as to rotate the motor by about 
    #one revolution and stop it at the final position.
    #Note: 16,384 encoder ticks per revolution
    while True:
        var.run(setp_init, timtimeint)
        yield 0

def task4_fun():
    """!
    Task which runs the controller for motor #2. 
    
    """
    #loop to run multiple Kp values for one rotation each 
    
    #runs the controller, running closed-loop step response tests 
    #in which the setpoint is changed so as to rotate the motor by about 
    #one revolution and stop it at the final position.
    #Note: 16,384 encoder ticks per revolution
    while True:
        var2.run(setp_init, timtimeint)
        yield 0
    
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

#--------------Initializing-Motor-#1--------------------------------------------------------------
 
    ena = pyb.Pin.board.PC1
    in1 = pyb.Pin.board.PA0
    in2 = pyb.Pin.board.PA1
    motimer = 5

    #encoder init
    cp1 = pyb.Pin.board.PC6
    cp2 = pyb.Pin.board.PC7
    cptimer = 8
    Kp_init = 0.05
    setp_init = 16384


    #establish controller class
    var = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

    #Kp_init = float(input("Input a Kp: "))
    Kp_init = 0.05
    #zero the encoder count and position
    var.zero()
    var.set_Kp(Kp_init)
    timtimeint = utime.ticks_ms()
    
    var.moe.set_duty_cycle(0)

#--------------Initializing-Motor-#2--------------------------------------------------------------

    ena = pyb.Pin.board.PA10
    in1 = pyb.Pin.board.PB4
    in2 = pyb.Pin.board.PB5
    motimer = 3

    #encoder init
    cp1 = pyb.Pin.board.PB6
    cp2 = pyb.Pin.board.PB7
    cptimer = 4
    Kp_init = 0.05
    setp_init = 16384

    #establish controller class
    var2 = controller.P_Control(Kp_init, setp_init, 0, motimer, ena, in1, in2, cp1, cp2, cptimer)

    #Kp_init = float(input("Input a Kp: "))
    Kp_init = 0.05
    #zero the encoder count and position
    var2.zero()
    var2.set_Kp(Kp_init)
    timtimeint = utime.ticks_ms()

    var2.moe.set_duty_cycle(0)
#-------------------------------------------------------------------------------------------------------   
    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    #task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=10,
                        #profile=True, trace=False, shares=(share0, q0))
    #task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=10,
                        #profile=True, trace=False, shares=(share0, q0))
    task3 = cotask.Task(task3_fun, name="Task_3", priority=3, period=100,
                        profile=True, trace=False)
    task4 = cotask.Task(task4_fun, name="Task_4", priority=4, period=100,
                        profile=True, trace=False)
    #cotask.task_list.append(task1)
    #cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

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
    var.print_res()
    #var2.print_res()