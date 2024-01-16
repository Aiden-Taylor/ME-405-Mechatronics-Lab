#import relevant modules 

import time
import micropython
micropython.alloc_emergency_exception_buf(100)

#define pin names 

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

pinB0ADC = pyb.ADC(pyb.Pin.board.PC0)


QUEUE_SIZE = 42
int_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation

#create interrupt

def timer_int(tim_num):
    
    int_queue.put()    



#create step response function 

def step_response(): #how you define a function
    pinC0.value(1)


if __name__ == "__main__":

    step_response(...parameters...)

