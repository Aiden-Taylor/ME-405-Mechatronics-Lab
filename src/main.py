import motor_driver

if __name__ == "__main__":
    # Script code goes here
    enpin = 0
    a_pin = 0
    another_pin = 0
    a_timer = 3
    moe = motor_driver.MotorDriver(enpin, a_pin, another_pin, a_timer)
    while True:
        moe.set_duty_cycle(int(input('set a duty cycle')))
        # moe.set_duty_cycle(0)