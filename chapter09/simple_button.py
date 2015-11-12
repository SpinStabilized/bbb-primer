import Adafruit_BBIO.GPIO as GPIO
import time

# Define program constants
BUTTON_PIN = 'P9_11'
OFF        = 0
ON         = 1

# Configure the GPIO pin and set the initial state of variables to track the
# state of the button.
GPIO.setup(BUTTON_PIN, GPIO.IN)
button_state_old = OFF 
button_state_new = OFF

# print out a nice message to let the user know how to quit.
print('Starting, press <control>-c to quit.\n')

# Execute until a keyboard interrupt
try:
    while True:
    	# Check the state of the pin. If it is different than the last state,
    	# print a message.
    	button_state_new = GPIO.input(BUTTON_PIN)
    	if button_state_new != button_state_old:
    		if button_state_new == OFF:
    			print('Button transitioned from off to on.')
    		else:
    			print('Button transitioned from on to off.')
        
        # Update the stored button state and then wait a tenth of a second.
        button_state_old = button_state_new
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
