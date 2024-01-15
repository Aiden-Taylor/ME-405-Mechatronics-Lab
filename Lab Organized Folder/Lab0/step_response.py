
#import relevant modules

import time
import micropython
micropython.alloc_emergency_exception_buf(100)

#define pin names 

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

pinB0ADC = pyb.ADC(pyb.Pin.board.PC0)

#create interrupt

def timer_int(tim_num):
    
    



#create step response function 

def step_response(): #how you define a function
    pinC0.value(1)
    tim = 0
    val = 0
    while val < 3.4:
        time.sleep_ms(10) #sleeps for 10 ms 
        tim += 10         #indicate that 10 seconds has passed
        val = pinB0ADC.read()/3.3
        print(tim, ",", val)
        
#implement function if the file is called main
        
if __name__ == "__main__":
    step_response()
