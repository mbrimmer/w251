import paho.mqtt.client as mqtt
import numpy as np
import cv2 as cv
import sys

MQTT_HOST="test.mosquitto.org"
MQTT_PORT=1883
MQTT_TOPIC="mb_faces/#"

OUTPUT_DIR = '/OUTPUT_DIR'

img_num = 0

def on_connect_local(client, userdata, flags, rc):
        print("Connected to broker with rc: " + str(rc))
        client.subscribe(MQTT_TOPIC)

def on_message(client,userdata, msg):
  global img_num
  try:
    print("message received!")
    img = np.fromstring(msg.payload, dtype='uint8')
    img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)

    # print shape to ensure we received a reasonable size image
    # print('img shape:', img.shape)
    # write face to local director to ensure it's properly receiving

    if(img_num <10):
      img_name = OUTPUT_DIR + "/face-0" + str(img_num) + ".png"
      print(img_name)
    else:
      img_name = OUTPUT_DIR + "/face-" + str(img_num) + ".png"
      print("image name:",img_name)

    print('Writing File ...')
    cv.imwrite(img_name, img)
    print('Finished Writing File')


    img_num += 1
  except:
    print("Unexpected error:", sys.exc_info()[0])

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect_local
mqttclient.connect(MQTT_HOST, MQTT_PORT, 60)
mqttclient.on_message = on_message



# go into a loop
mqttclient.loop_forever()
