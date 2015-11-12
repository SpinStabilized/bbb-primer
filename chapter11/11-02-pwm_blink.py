import Adafruit_BBIO.PWM as PWM

LED_PIN   = 'P9_14'
FREQUENCY = 1000  # Hz

if __name__ == '__main__':

    try:
        PWM.start(LED_PIN, 50, FREQUENCY)

        while True:
            pass

    except KeyboardInterrupt:
        PWM.stop(LED_PIN)
        PWM.cleanup()
