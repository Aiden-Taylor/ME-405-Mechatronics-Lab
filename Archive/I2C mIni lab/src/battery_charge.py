import pyb
import utime
import set_leds

S0_OFF = 0
S1_ON = 1
S2_DISP = 2
S3_LOW_B = 3
S4_CHARGING = 4

class battery_charge():

    def __init__(self, task_name):
        # A variable to indicate what state the FSM
            # is about to run
            state = 0
            self.plug_pin = PB1
            self.plugged = pyb.Pin.read(self.plug_pin)
            self.on = 0

            # Create OFF LED mask
            self.led_off = 0b00000000

            # Create ON LED mask
            self.led_on = 0b11111111

            # Boolean variable to tell if ON blink has already happened
            self.on_blink = 0
            
            #setup plug and button pins!!!

            # Battery charge pin
            self.pinB0ADC = pyb.ADC(pyb.Pin.board.PB0)

    def task_gen_fun(self, task_name):
        
        while(True):
            # Implement FSM inside while loop
            if (state == S0_OFF):
                # Establish LED class
                var = set_leds.LED(self.led_off)
                # Turn off all LEDs
                var.led(self.led_off)
                # Set on value
                self.on = 0
                # If button is pressed for more than 2 seconds turn off the LEDs
                if self.button == True:
                    start_time = utime.ticks_ms()
                    while self.button == True:
                        count_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
                        if count_ms > 2000:   
                            state = S1_ON
                            break
                # If battery is plugged in move to charging state
                if self.plugged == True:
                    state = S4_CHARGING            
            elif (state == S1_ON):
                # Set on value
                self.on = 1
                # Blink all LEDs 3 times quickly
                if self.on_blink == 0:
                    for n in range(2):
                        var.led(self.led_on)
                        utime.sleep_ms(250)
                        var.led(self.led_off)
                        utime.sleep_ms(250)
                    self.on_blink = 1
                # Logic fo determining button input
                if self.button == True:
                    start_time = utime.ticks_ms()
                    while self.button == True:
                        count_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
                    # If button is pressed for more than 2 seconds turn off the LEDs
                    if count_ms > 2000:  
                        state = S0_OFF
                    # If button is pressed for less than 1 seconds display battery charge
                    elif count_ms < 1000:
                        state = S2_DISP
                # If battery is plugged in move to charging state
                if self.plugged == True:
                    state = S4_CHARGING

            elif (state == S2_DISP):
                # Read the analog voltage from the battery on pinB0
                # ADC has a max value of 4095
                percent_charge = (self.pinB0ADC.read()/4095)*100
                if percent_charge < 12.5:
                    state = S3_LOW_B
                led_num = percent_charge/12.5
                led_disp = 0
                for n in range(led_num-1):
                    led_disp = led_disp | 1<<n
                var.led(led_disp)
                utime.sleep_ms(1000)
                var.led(self.led_off)
                state = S1_ON
                    
            elif (state == S3_LOW_B):
                # Blink all LEDs 4 times quickly
                for n in range(3):
                    var.led(self.led_on)
                    utime.sleep_ms(250)
                    var.led(self.led_off)
                    utime.sleep_ms(250)
                state = S1_ON

            elif (state == S4_CHARGING):
                # Read the analog voltage from the battery on pinB0
                # ADC has a max value of 4095
                percent_charge = (self.pinB0ADC.read()/4095)*100
                if percent_charge < 12.5:
                    state = S3_LOW_B
                led_num = percent_charge/12.5
                led_disp = 0
                led_pend = 0
                for n in range(led_num-1):
                    led_disp = led_disp | 1<<n
                for n in range(led_num):
                    led_pend = led_pend | 1<<n
                # Display the battery charge and blink the pending LED
                var.led(led_disp)
                utime.sleep_ms(250)
                var.led(led_pend)
                utime.sleep_ms(250)
                # If battery is unplugged retreat back to correct state
                if self.plugged == 0 & self.on == 0:
                    state = S0_OFF
                if self.plugged == 0 & self.on == 1:
                    state = S1_ON

            else:
                # If the state isnt 0, 1, or 2 we have an
                # invalid state
                raise ValueError('Invalid state')
                
            yield state
                
            break

def main():
        
        while True:
            try:
                # Run the generator
                next(battery_charge)
                    # Sleeping (delaying) for 1/2 second to slow down
                # the printing
                utime.sleep(0.5)
            
            # Trying to catch the "Ctrl-C" keystroke to break out
            # of the program cleanly
            except KeyboardInterrupt:
    
                # Once the program is over, do any sort of cleanup as needed
                print('Program terminated')

# THe following block prevents main() from running when the file
# is imported instead of run as a main program
if __name__ == '__main__':
    main()