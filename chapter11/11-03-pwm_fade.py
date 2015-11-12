import Adafruit_BBIO.PWM as PWM
import time

LED_PIN = 'P9_14'
PWM_FREQUENCY = 1000  # Hz
BLINK_FREQUENCY = 1   # Hz

if __name__ == '__main__':
    step_size = 1
    brightness = 0
    fade_wait = ((1/float(BLINK_FREQUENCY))/2) / (100/float(step_size))
    PWM.start(LED_PIN, 0, PWM_FREQUENCY)

    try:
        while True:

            while brightness < 100:
                brightness = brightness + step_size
                PWM.set_duty_cycle(LED_PIN, brightness)
                time.sleep(fade_wait)

            while brightness > 0:
                brightness = brightness - step_size
                PWM.set_duty_cycle(LED_PIN, brightness)
                time.sleep(fade_wait)

    except KeyboardInterrupt:
        PWM.stop(LED_PIN)
        PWM.cleanup()
