""" 
rr_crossing_blinkers.py - Python File to blink LEDs attached to 
                          GPIO P9_12 and P9_15.

Example program for "The BeagleBone Black Primer"
"""

import Adafruit_BBIO.GPIO as bbb     # Declare a bbb variable, board H/W object
from twisted.internet import task, reactor

state1 = bbb.LOW                     # Declare a variable to represent GPIO P9_12 state
state2 = bbb.LOW                     # Declare a variable to represent GPIO P9_15 state

bbb.setup("P9_12", bbb.OUT)          # Set the GPIO P9_12 control to output
bbb.setup("P9_15", bbb.OUT)          # Set the GPIO P9_15 control to output

def blink():
	""" Function - blink
	Toggle the value of the state variables between high and low when called.
	"""
	global state1
	global state2

	if state1 is bbb.LOW:            # If P9_12 is LOW..
		state1 = bbb.HIGH            # ... set P9_12 to HIGH
		state2 = bbb.LOW             # ... set P9_15 to LOW
	else:                            # Otherwise...
		state1 = bbb.LOW             # ... set P9_12 to LOW
		state2 = bbb.HIGH            # ... set P9_15 to HIGH

	bbb.output("P9_12", state1)      # Update the GPIO P9_12 state
	bbb.output("P9_15", state2)      # Update the GPIO P9_15 state

timer_call = task.LoopingCall(blink) # ...
timer_call.start(1)                  # Alternate blinking LEDs every 1 second
reactor.run()                        # ...
