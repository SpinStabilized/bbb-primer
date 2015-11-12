""" 
binary_counter.py - Illuminate 8 LEDs as binary number representation.

Example program for "The BeagleBone Black Primer"
"""

import Adafruit_BBIO.GPIO as GPIO 
import time

PINS = ['P9_22', 'P9_21', 'P9_16', 'P9_15',
        'P9_14', 'P9_13', 'P9_12', 'P9_11']

def check_bit(number, bit):
	return (number & (1 << bit)) != 0

for pin in PINS:                     # Configure all the pins to output & off
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

print 'Binary Counter - <ctrl>-c to exit.'

try:
	for i in range(256):
		for bit, pin in enumerate(PINS):
			if check_bit(i, bit):
				GPIO.output(pin, GPIO.HIGH)
			else:
				GPIO.output(pin, GPIO.LOW)

		time.sleep(0.1)
	time.sleep(5)

except KeyboardInterrupt:
	pass

finally:
	print 'Done! Clearing bits...'
	for pin in PINS:
		GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()
