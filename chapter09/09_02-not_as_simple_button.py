import Adafruit_BBIO.GPIO as GPIO
import time
import subprocess

# Define program constants
BUTTON_PIN = 'P9_11'
LED_PIN    = 'P9_12'

# Configure the GPIO pins and set the initial state of variables to track the
# state of the button.
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# print out a nice message to let the user know how to quit.
print('Starting, press <control>-c to quit.\n')

# Execute until a keyboard interrupt
try:
	while True:
		# Wait for the BUTTON_PIN to have a falling edge, indicating the
		# button has been pressed.
    	GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)

    	# Button has been pressed so turn on the LED and start your program
    	GPIO.output(LED_PIN, GPIO.HIGH)
    	subprocess.call(['/path/to/the/program', '-argument'])

    	# Program is done, turn off the LED and start waiting again.
    	GPIO.output(LED_PIN, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
