import paho.mqtt.client as mqtt
import numpy as np
import cv2 as cv
import sys

LOCAL_MQTT_HOST="test.mosquitto.org"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="mb_faces/#"

OUTPUT_DIR = '/HW03/FACES/'

global img_num = 0

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  try:
    print("message received!".format(msg))
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    face = cv.imdecode(msg.payload.decode(), cv.COLOR_BGR2GRAY) 
    
    # write face to local director to ensure it's properly receiving
    if(img_num <10):
      img_name = OUTPUT_DIR + "/face-0" + str(img_num) + ".png"
      print(img_name)
    else:
      img_name = OUTPUT_DIR + "/face-" + str(img_num) + ".png"
      print(img_name)
    cv.imwrite(img_name, face)
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    
    img_num += 1
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
