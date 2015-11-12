import bbbservo
import time

PAN_PIN = 'P9_14'
TILT_PIN = 'P8_13'


if __name__ == '__main__':
    try:

        while True:
            # Configure and initialize out pan/tilt mechanism servos
            pan_servo = bbbservo.Servo('P9_14', 0,
                                       servo_range=(-90, 90),
                                       ppm_range=(0.4, 2.25))
            tilt_servo = bbbservo.Servo('P8_13', 0,
                                        servo_range=(-90, 90),
                                        ppm_range=(0.8, 2.25))

            pan_servo.position = 0
            tilt_servo.position = 0

    except KeyboardInterrupt:

        pan_servo.position = 0
        tilt_servo.position = 0
        time.sleep(1)
        pan_servo.cleanup()
        tilt_servo.cleanup()
