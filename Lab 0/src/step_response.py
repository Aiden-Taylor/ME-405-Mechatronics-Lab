#import relevant modules 

import pyb 
from queue import Queue
import micropython
micropython.alloc_emergency_exception_buf(100)

#define pin names 

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
pinB0ADC = pyb.ADC(pyb.Pin.board.PC0)

#initialize queue 

QUEUE_SIZE = 42
#time_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation
#value_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation

time_q = Queue()
value_q = Queue()

#create interrupt

def timer_int(tim_num):
    
    time_queue.put(tim_num.counter())
    val = pinB0ADC.read()/3.3
    value_queue.put(val)


#create step response function 

def step_response(period): #how you define a function
    tim = pyb.Timer(4, freq=10)      # create a timer object using timer 4 - trig
    pinC0.value(1)
    
    for period:
        tim.callback(timer_int)              # set the callback to our tick function

print(timer_queue,value_queue)
    

#if __name__ == "__main__":

step_response(20)

