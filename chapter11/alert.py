import Adafruit_BBIO.GPIO as GPIO
import time

MTR_PIN   = 'P9_11'
FREQUENCY = 1  # Hz

if __name__ == '__main__':

    GPIO.setup(MTR_PIN, GPIO.OUT)
    GPIO.output(MTR_PIN, GPIO.LOW)

    # Pulse for 0.5 seconds
    GPIO.output(MTR_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(MTR_PIN, GPIO.LOW)

    GPIO.output(MTR_PIN, GPIO.LOW)
    GPIO.cleanup()
