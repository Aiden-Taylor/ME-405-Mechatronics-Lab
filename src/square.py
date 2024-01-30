pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

pinB0ADC = pyb.ADC(pyb.Pin.board.PC0)

import time 

while True: #cap T True is the boolean value true
    
        pinC0.value(1)
        time.sleep(5)  #waits for five seconds
        print(pinB0ADC.read())
        pinC0.value(0)
        time.sleep(5)
        print(pinB0ADC.read())
        