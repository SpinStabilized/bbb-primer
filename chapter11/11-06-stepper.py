import Adafruit_BBIO.GPIO as GPIO
import time
import ctypes

libc = ctypes.CDLL('libc.so.6')

STEP_PIN = 'P9_11'
DIR_PIN = 'P9_12'
MICROSTEPS = 8


def move(steps, speed):
    ''' Move the stepper so many steps at a specific rate

    Keyword arguments:
    steps -- Number of steps to move
    speed -- Time for a full step (milliseconds)

    Note: This function commands step signal pulses. This may not control
          full step motions depending upon any microstepping defined in the
          control.
    '''
    if steps > 0:
        GPIO.output(DIR_PIN, GPIO.HIGH)
    else:
        GPIO.output(DIR_PIN, GPIO.LOW)

    steps = abs(steps)

    delay = ((float(speed) / 2) / MICROSTEPS) * 1000

    steps_remaining = steps
    while steps_remaining > 0:

        GPIO.output(STEP_PIN, GPIO.HIGH)
        libc.usleep(int(delay))

        GPIO.output(STEP_PIN, GPIO.LOW)
        libc.usleep(int(delay))

        steps_remaining = steps_remaining - 1


def move_degrees(degrees, speed, degrees_per_step=1.8, usteps_per_step=8):
    ''' Move the stepper so many degrees at a specific rate

    Keyword arguments:
    degrees          -- Number of degrees to move
    speed            -- Time for a full step (milliseconds)
    degrees_per_step -- Number of degrees in 1 full step (1.8 default)
    usteps_per_step  -- Number of microsteps per step in the driver

    '''
    steps = degrees / (degrees_per_step / usteps_per_step)
    move(steps, speed)

if __name__ == '__main__':

    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.output(STEP_PIN, GPIO.LOW)

    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.output(DIR_PIN, GPIO.HIGH)

    try:

        move_degrees(90, 100)
        time.sleep(1)
        move_degrees(-90, 100)
        time.sleep(1)
        move_degrees(360, 10)
        time.sleep(1)
        move_degrees(-360, 2.64)
        time.sleep(1)
        move_degrees(360*2, 3)
        time.sleep(1)
        move_degrees(-360, 2.64)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.output(STEP_PIN, GPIO.LOW)
        GPIO.cleanup()
