#import relevant modules 

import machine 
import time
import micropython
micropython.alloc_emergency_exception_buf(100)

#define pin names 

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

pinB0ADC = pyb.ADC(pyb.Pin.board.PC0)

#initialize queue 

QUEUE_SIZE = 42
time_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation
value_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation

#create interrupt

def timer_int(tim_num):
    
    machine.enable_irq()
    time_queue.put(tim_num)
    val = pinB0ADC.read()/3.3
    value_queue.put(val)



#create step response function 

def step_response(): #how you define a function
    pinC0.value(1)
    

if __name__ == "__main__":

    step_response(...parameters...)

