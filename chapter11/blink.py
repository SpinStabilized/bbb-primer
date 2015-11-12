import Adafruit_BBIO.GPIO as GPIO
import time

LED_PIN   = 'P9_11'
FREQUENCY = 1 # Hz

if __name__ == '__main__':

	state = GPIO.LOW 
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN, state)

	try:
		while True:
			if state is GPIO.LOW:
				state = GPIO.HIGH
			else:
				state = GPIO.LOW

			GPIO.output(LED_PIN, state)
			time.sleep(0.25)

	except KeyboardInterrupt:
		GPIO.output(LED_PIN, GPIO.LOW)
		GPIO.cleanup()