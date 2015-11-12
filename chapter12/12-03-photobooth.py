import Adafruit_BBIO.GPIO as GPIO
import cv2
import time
from datetime import datetime

# Define program constants
BUTTON_PIN = 'P9_11'
MAIN_WINDOW = 'BeagleBone Black Photobooth'
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'

if __name__ == '__main__':
    try:
        # Configure the GPIO pin and add an event watch to check if
        # the button has been pressed
        GPIO.setup(BUTTON_PIN, GPIO.IN)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)

        # Configure the video device for capture, -1 indicates
        # the default, in our case, /dev/video0
        video_capture = cv2.VideoCapture(-1)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            # Display the resulting frame
            cv2.imshow(MAIN_WINDOW, frame)

            # If the button has been pressed
            if GPIO.event_detected(BUTTON_PIN):

                # Grab the current time for a timestamp in the filename
                # and generate the file path & name
                snap_time = datetime.now().strftime(TIMESTAMP_FORMAT)
                output_file = 'snaps/snap_{}.jpeg'.format(snap_time)

                # Configure the output to be a JPEG with a 90% image quality
                jpeg_settings = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

                # Write the frame to the file
                cv2.imwrite(output_file, frame, jpeg_settings)

                # Wait for an extra second with the captured frame displayed
                # to give a little feedback to the user
                time.sleep(1)

            cv2.waitKey(1)

    except KeyboardInterrupt:
        # Clean-up
        video_capture.release()
        cv2.destroyAllWindows()
