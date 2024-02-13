"""! @file led.py
  The led file being used for the led pwm control
  """

#import relevant modules 

import pyb 
import cqueue
import micropython
import time

micropython.alloc_emergency_exception_buf(100)


def led_setup():
    """!
      The led_setup function initializes the timer, channel, and corresponding pin. Timer 2 channel 1 will be used, along with pin A0. The 
      timer channel is set to the PWM_INVERTED mode. 
      """
    
    #set pin PA0 as an output
    pinA0 = pyb.Pin((pyb.Pin.board.PA0), pyb.Pin.OUT_PP)

    #create timer 2 on channel 1 to work with pin A0 
    tim2 = pyb.Timer(2, freq=20000)
    global ch1
    ch1 = tim2.channel(1, pyb.Timer.PWM_INVERTED, pin=pinA0)

def led_brightness(brightness):
    """!
      The led_brightness function sets the brightness of the LED by acccepting the desired brightness 
      percentage as a parameter and sending it to the ch1.pulse_width_percent() command. 
      """
    
    #set the pulse width percentage 
    ch1.pulse_width_percent(brightness)  
    
if __name__ == "__main__":
    # Script code goes here
    led_setup()
    while True:
        led_brightness(0)
        for n in range(100):
            time.sleep(.05)
            led_brightness(n)
