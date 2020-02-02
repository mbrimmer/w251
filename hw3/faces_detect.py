"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display
(will publish to mosquitto broker in future)

Calling method: python3 faces_video.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as paho
import sys

# Check Arguments / Proper Usage
if (len(sys.argv) != 2):
    print("Error! - Usage: python3 face_detect.py <broker_address>")
    exit()
else:
    broker_addr = sys.argv[1]

#Debug mode / flag
CONNECT_TO_CLIENT=True
DEBUG=True

# Set up connection to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection to broker: Success!")
    else:
        print("Connection to broker: Failed!")

if CONNECT_TO_CLIENT:
    # Connect to client
    client = paho.Client()
    #attach function to callback
    client.on_connect = on_connect
    client.connect(broker_addr, 1883, 60)

    # make sure there is time for client to come up
    time.sleep(2)


cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0

if CONNECT_TO_CLIENT:
    client.loop_start()

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
            print(f"Image: {img_num}, payload={coord_payload}")
        if CONNECT_TO_CLIENT:
            client.publish("mb_faces/coord_msg", coord_payload)
            # Publish Actual Image
            # client.publish("mb_face_app/msg", bytearray(cv.imencode('.png', crop_faces)[1]), qos=1)
        img_num+=1

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(1)
client.loop_stop()
client.disconnect()
cap.release()
cv.destroyAllWindows()
