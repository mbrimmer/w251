"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display
(will publish to mosquitto broker in future)

Calling method: python3 faces_video.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(1)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get Images
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    # gray here is the gray frame from camera
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Display image, faces, and publish message
    img = cv.imshow('frame', gray)
    for (x,y,w,h) in faces:
        crop_faces = gray[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Time to wait next command, avoid blockage
time.sleep(1)

cap.release()
cv.destroyAllWindows()
