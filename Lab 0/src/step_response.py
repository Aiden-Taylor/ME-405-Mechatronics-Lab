#import relevant modules 

import pyb 
import cqueue
import micropython
micropython.alloc_emergency_exception_buf(100)

#define pin names 

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
pinB0ADC = pyb.ADC(pyb.Pin.board.PB0)

#initialize queues 

QUEUE_SIZE = 200
time = [] #empty time list
value_queue = cqueue.IntQueue(QUEUE_SIZE) #from 405 library documentation

for i in range(QUEUE_SIZE):
    time.append(0.01*i)
    
    #while printing create the time variables 
    
tim = pyb.Timer(2, freq=100)      # create a timer object using timer 4 - trig

#create interrupt

def timer_int(tim_num):
    
    #time_queue.put(tim_num.counter())
    val = pinB0ADC.read()
    value_queue.put(val)
    
    if value_queue.full():
        tim.callback(None)


#create step response function 

def step_response():                 
    pinC0.value(0)
    tim.callback(timer_int)          # set the callback to our timer_int function
    pinC0.value(1)
    
    while not value_queue.full():
        pass              
    
    #run a for loop through time run get on the queue
    for val in time:
        print(f"{val},{value_queue.get(val)) #not sure if this is correct     
    #print(value_queue)
    print("end")
    

if __name__ == "__main__": #only runs if its the main program 
    step_response()

