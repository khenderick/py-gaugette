#----------------------------------------------------------------------
# Gaugette.GPIO from from https://github.com/guyc/py-gaugette
# Guy Carpenter, Clearwater Software
#
# This is an abstraction layer for GPIO calls to isolate the
# differences between the RasperryPi and BeagleBone Black implementations.
#
# On the RPi, we use wiringpi2.GPIO
# On the BBB, we use Adafruit_BBIO.GPIO
#
#----------------------------------------------------------------------
import gaugette


class GPIO:
    def __init__(self):
        if gaugette.platform == 'raspberrypi':
            import wiringpi2
            self.gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
            self.setup = self.wiringpi2_setup
            self.output = self.gpio.digitalWrite
            self.input = self.gpio.digitalRead
            self.OUT = self.gpio.OUTPUT
            self.IN = self.gpio.INPUT
            self.HIGH = self.gpio.HIGH
            self.LOW = self.gpio.LOW
            self.PUD_UP = self.gpio.PUD_UP
            self.PUD_DOWN = self.gpio.PUD_DOWN
            self.PUD_OFF = self.gpio.PUD_OFF

        elif gaugette.platform == 'beaglebone':
            import Adafruit_BBIO.GPIO
            self.gpio = Adafruit_BBIO.GPIO
            self.setup = self.gpio.setup
            self.output = self.gpio.output
            self.input = self.gpio.input
            self.OUT = self.gpio.OUT
            self.IN  = self.gpio.IN
            self.HIGH = self.gpio.HIGH
            self.LOW = self.gpio.LOW
            self.PUD_UP = self.gpio.PUD_UP
            self.PUD_DOWN = self.gpio.PUD_DOWN
            self.PUD_OFF = self.gpio.PUD_OFF

        elif gaugette.platform == 'micropython':
            import pyb
            self.iomap = {}

            def _setup(pin, direction):
                if pin not in self.iomap:
                    self.iomap[pin] = pyb.Pin(pin, direction, pyb.Pin.PULL_DOWN)

            def _output(pin, value):
                if value:
                    self.iomap[pin].high()
                else:
                    self.iomap[pin].low()

            def _input(pin):
                return self.iomap[pin].value()

            self.gpio = None  # Not yet implemented
            self.setup = _setup
            self.output = _output
            self.input = _input
            self.OUT = pyb.Pin.OUT_PP
            self.IN = pyb.Pin.IN
            self.HIGH = True
            self.LOW = False
            self.PUD_UP = None
            self.PUD_DOWN = None
            self.PUD_OFF = None

        else:
            raise NotImplementedError("Platform '%s' is not supported." % gaugette.platform)

    #----------------------------------------------------------------------

    # Implement the setup call via the wiringpi2 API
    def wiringpi2_setup(self, channel, direction, pull_up_down=None):
        self.gpio.pinMode(channel, direction)
        if pull_up_down is None: pull_up_down = self.gpio.PUD_OFF
        self.gpio.pullUpDnControl(channel, pull_up_down)
