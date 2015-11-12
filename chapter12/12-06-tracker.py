import Adafruit_BBIO.GPIO as GPIO
import bbbservo
import cv2
import time
from datetime import datetime

# Define BBB Pin Constants
BUTTON_PIN = 'P9_11'
PAN_PIN = 'P9_14'
TILT_PIN = 'P8_13'

# Field of view of the camera
FOV = 75

if __name__ == '__main__':
    try:
        # Configure the GUI
        window_name = 'Camera Tracker'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        # Configure the snapshot button
        GPIO.setup(BUTTON_PIN, GPIO.IN)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)

        # Set up the identification cascade to use
        cascade = '/root/opencv/data/lbpcascades/lbpcascade_frontalface.xml'
        face_cascade = cv2.CascadeClassifier(cascade)

        # Define some basic camera frame properties and relationships
        camera = cv2.VideoCapture(-1)
        cam_frame_size = (camera.get(cv2.CAP_PROP_FRAME_WIDTH),
                          camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cam_frame_center = (cam_frame_size[0] / 2, cam_frame_size[1] / 2)
        pos_to_angle = ((FOV / 2) / cam_frame_center[0],
                        (FOV / 2) / cam_frame_center[1])

        # Configure and initialize out pan/tilt mechanism servos
        pan_servo = bbbservo.Servo('P9_14', 0,
                                   servo_range=(-90, 90),
                                   ppm_range=(0.4, 2.25))
        tilt_servo = bbbservo.Servo('P8_13', 0,
                                    servo_range=(-90, 90),
                                    ppm_range=(0.8, 2.25))
        time.sleep(1)  # Wait for servo motion to complete

        # Initialize a couple other parameters we will use
        last_found = time.time()

        while True:

            # Capture frame-by-frame
            ret, frame = camera.read()

            # Create a reduced copy of the frame and convert it to grey
            reduced = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            reduced_gray = cv2.cvtColor(reduced, cv2.COLOR_BGR2GRAY)

            # Find the faces in the reduced, grayscale, image
            faces = face_cascade.detectMultiScale(reduced_gray, 1.3, 2)

            for i, (x, y, w, h) in enumerate(faces):
                origin = (x * 2, y * 2)
                face_center = (origin[0] + w, origin[1] + h)

                if i == 0:
                    cv2.circle(frame, face_center, w, (0, 255, 0), 1)
                    center_delta = (cam_frame_center[0] - face_center[0],
                                    cam_frame_center[1] - face_center[1])
                    pan_servo.position = center_delta[0] * pos_to_angle[0]
                    tilt_servo.position = center_delta[1] * pos_to_angle[1]
                    last_found = time.time()
                else:
                    cv2.circle(frame, face_center, w, (0, 0, 255), 1)

            # Otherwise, zero the platform if we haven't seen any faces for
            # a specified number of seconds
            else:
                if time.time() - last_found > 5:
                    pan_servo.position = 0
                    tilt_servo.position = 0

            # If the button has been pressed
            if GPIO.event_detected(BUTTON_PIN):

                # Grab the current time for a timestamp in the filename
                # and generate the file path & name
                snap_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                output_file = 'snaps/snap_{}.jpeg'.format(snap_time)
                jpeg_settings = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

                # Write the frame to the file
                cv2.imwrite(output_file, frame, jpeg_settings)

            # Display the resulting frame
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        pan_servo.position = 0
        tilt_servo.position = 0
        time.sleep(1)
        pan_servo.cleanup()
        tilt_servo.cleanup()
