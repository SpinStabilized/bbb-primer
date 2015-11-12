import Adafruit_BBIO.PWM as PWM
import time

SERVO_PIN = 'P9_14'
ANGLE_RANGE = [0, 180]  # degrees
PPM_RANGE = [0.486, 2.25]  # milliseconds
PPM_FREQUENCY = 50  # Hertz


def ppm_to_pwm(ppm, frequency):
    ''' Convert from a PPM pulse width to a PWM duty cycle

    Keyword arguments:
    ppm       -- PPM pulse width in milliseconds
    frequency -- PPM frequency in Hertz

    Return:
    PWM duty cycle as a percent over 0 to 100
    '''
    return ((ppm / 1000) * frequency) * 100

if __name__ == '__main__':

    try:
        # Calculate some variables needed in angle calculation
        angle_delta = ANGLE_RANGE[1] - ANGLE_RANGE[0]
        ppm_delta = PPM_RANGE[1] - PPM_RANGE[0]
        ppm_per_degree = ppm_delta / float(angle_delta)

        # Initialize the PWM and go to the lowest PPM
        start_position = ppm_to_pwm(PPM_RANGE[0], PPM_FREQUENCY)
        PWM.start(SERVO_PIN, start_position, PPM_FREQUENCY)
        time.sleep(1)  # Wait for servo motion to complete

        # Work through the full range of positions
        for angle in range(ANGLE_RANGE[0], ANGLE_RANGE[1]):
            relative_angle = angle - ANGLE_RANGE[0]
            relative_ppm = relative_angle * ppm_per_degree
            absolute_ppm = relative_ppm + PPM_RANGE[0]
            duty_cycle = ppm_to_pwm(absolute_ppm, PPM_FREQUENCY)
            PWM.set_duty_cycle(SERVO_PIN, duty_cycle)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        PWM.stop(SERVO_PIN)
        PWM.cleanup()
