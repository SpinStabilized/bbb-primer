import Adafruit_BBIO.PWM as PWM


class Servo(object):
    '''Object representing a servo motor utilizing the Adafruit_BBIO library.

    This class defines an object to manipulate a servo motor on a BeagleBone
    Black (BBB). The class utilizes the PWM module of the Adafruit_BBIO library
    for pulse width manipulation.

    Attributes:
        pin (string): The physical pin on the BBB (i.e. 'P9_14')
        servo_range (tuple): Max and min of servo range in degrees
        ppm_range (tuple): Max and min of the PPM pulse width in milliseconds
        ppm_freq (number): Frequency of the PPM/PWM driver
        position (number): The position of the servo in degrees
        position_pulse_width (number): Position of the servo as pulse width
        position_duty_cycle (number): Position of the servo as a PWM duty cycle
        initialized (boolean): Object initialization status
    '''

    pin = ''
    '''BBB PWM pin in use'''

    servo_range = (0, 180)  # degrees
    '''Range of the servo in degrees'''

    ppm_range = (0.5, 2.5)
    '''Range of the PPM pulse width for servo control in milliseconds'''

    ppm_freq = 50
    '''PWM/PPM Driver frequency'''

    def __init__(self, pin, start, **kwargs):
        '''Initialize a Servo object.'''
        self.pin = pin

        for key in ('servo_range', 'ppm_range', 'ppm_freq'):
            if key in kwargs:
                setattr(self, key, kwargs[key])

        self.initialized = False
        self.position = start

    @property
    def position(self):
        '''Current servo position - assignment moves the servo'''
        return self._position

    @position.setter
    def position(self, value):
        if self.servo_range[0] <= value and value <= self.servo_range[1]:
            self._position = value
            if self.initialized:
                PWM.set_duty_cycle(self.pin, self._position_duty_cycle())
            else:
                PWM.start(self.pin, self._position_duty_cycle(), self.ppm_freq)
                self.initialized = True
        else:
            message_string = 'Servo commanded to {}. Valid range {}.'
            raise Exception(message_string.format(value, self.servo_range))

    def cleanup(self):
        '''Execute steps to clean up the PWM hardware'''
        PWM.stop(self.pin)
        PWM.cleanup()
        self.initialized = False

    def _position_duty_cycle(self):
        '''Current servo position as a PWM duty cycle'''
        ppm_delta = self.ppm_range[1] - self.ppm_range[0]
        range_delta = self.servo_range[1] - self.servo_range[0]
        pw_per_degree = ppm_delta / float(range_delta)
        relative_position = self.position - self.servo_range[0]
        relative_pulse_width = relative_position * pw_per_degree
        absolute_pulse_width = relative_pulse_width + self.ppm_range[0]
        pulse_width_seconds = absolute_pulse_width / float(1000)
        return (pulse_width_seconds * self.ppm_freq) * 100
