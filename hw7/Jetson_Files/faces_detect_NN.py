"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display
(will publish to mosquitto broker in future)

Calling method: python3 faces_video.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import time
import sys


DEBUG=True



cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0


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
        # Publish coordinates (debug)
        coord_payload = str(img_num)+ ':' + ' (' + str(x) + "," + str(y) + ')'
        if DEBUG:
            print(f"Image: {img_num}, payload={coord_payload} sent...")
        img_num+=1

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
