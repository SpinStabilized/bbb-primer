import Adafruit_BBIO.GPIO as GPIO
import subprocess

# Define program constants
BUTTON_PIN = 'P9_11'

# Configure the GPIO pin
GPIO.setup(BUTTON_PIN, GPIO.IN)

if __name__ == '__main__':

    # print out a nice message to let the user know how to quit.
    print('Starting snapshot program, press <control>-c to quit.\n')

    picture_count = 0

    # Execute until a keyboard interrupt
    try:
        while True:

            GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
            output_file = 'snaps/snap{:0>3}.jpeg'.format(picture_count)
            command_call = ['streamer', '-q', '-o', output_file]
            print('Click! Image saved to {}.'.format(output_file))
            subprocess.call(command_call)

            picture_count = picture_count + 1

    except KeyboardInterrupt:
        GPIO.cleanup()
