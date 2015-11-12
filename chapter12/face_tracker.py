import cv2

if __name__ == '__main__':

    # Define the name of a main window and create it
    main_window_name = 'BeagleBone Black Video'
    cv2.namedWindow(main_window_name, cv2.WINDOW_NORMAL)

    # Set up the identification cascade to use
    cascade = '/root/opencv/data/lbpcascades/lbpcascade_frontalface.xml'
    face_cascade = cv2.CascadeClassifier(cascade)

    # Configure the video device for capture, -1 indicates
    # the default, in our case, /dev/video0
    camera = cv2.VideoCapture(-1)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = camera.read()

            # Scale the frame down, convert it to grayscale, and then search
            # for faces.
            reduced = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            reduced_grey = cv2.cvtColor(reduced, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(reduced_grey, 1.3, 2)

            # Iterate over all the faces identified in the image and draw
            # rectangles around them.
            for (x, y, w, h) in faces:
                origin = (x * 2, y * 2)
                size = (w * 2, h * 2)
                far = (origin[0] + size[0], origin[1] + size[1])
                cv2.rectangle(frame, origin, far, (0, 0, 255), 2)

            # Display the resulting frame
            cv2.imshow(main_window_name, frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        # Clean everything up
        camera.release()
        cv2.destroyAllWindows()
