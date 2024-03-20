from pyb import I2C
from pyb import Pin

class LED:
    def __init__(self, leds_on):
        # Creating the object of the pyb.I2C class to configure the interface with the MCP23008
        self.mcp = I2C.init(1, I2C.CONTROLLER, baudrate = 100000)
        # I2C device address: 0100010 = 0x22

        # REGISTER 1-1: IODIR – I/O DIRECTION REGISTER (ADDR 0x00): Configure all GPIO pins as outputs
        self.led_io = bytearray(0b11111111) # 1 = output
        self.mcp.mem_write(self.led_io, 0x22, 0x00)

        # REGISTER 1-7: GPPU – GPIO PULL-UP RESISTOR REGISTER (ADDR 0x06): Disable all GPIO internal pull-up resistors
        self.pullups = bytearray(0b00000000) # 0 = disable
        self.mcp.mem_write(self.pullups, 0x22, 0x06)

        # Configuring the I2C SDA and SCL pins as their alternate functions
        # I2C requires external pullup resistors which are shown in the schematic
        self.pinPF0 = pyb.Pin(pyb.Pin.board.PF0, mode = pyb.Pin.AF_OD, alt = 4)
        self.pinPF1 = pyb.Pin(pyb.Pin.board.PF1, mode = pyb.Pin.AF_OD, alt = 4)

    def led(self, leds_on):
        # REGISTER 1-10: GPIO – GENERAL PURPOSE I/O PORT REGISTER (ADDR 0x09): Set GPIO states
        self.leds = bytearray([leds_on]) # LED bit mask
        self.mcp.mem_write(self.leds, 0x22, 0x09)        