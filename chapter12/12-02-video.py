import cv2

if __name__ == '__main__':

    # Define the name of a main window and create it
    main_window_name = 'BeagleBone Black Video'
    cv2.namedWindow(main_window_name, cv2.WINDOW_NORMAL)

    # Configure the video device for capture, -1 indicates
    # the default, in our case, /dev/video0
    video_capture = cv2.VideoCapture(-1)

    try:
        while True:
            # Capture a frame from the camera
            ret, frame = video_capture.read()

            # Display the frame in our window
            cv2.imshow(main_window_name, frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        # Clean everything up
        video_capture.release()
        cv2.destroyAllWindows()
