"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display

Calling method: python3 faces_detect_NN.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import time
import sys
import math


from PIL import Image
import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
from tf_trt_models.detection import download_detection_model, build_detection_graph

DEBUG=False

FROZEN_GRAPH_NAME='data/frozen_inference_graph_face.pb'

output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())

# https://github.com/NVIDIA-AI-IOT/tf_trt_models/blob/master/tf_trt_models/detection.py
INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)


tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')

cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0

# Get Images
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    img = cv.imshow('frame', frame)

    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections],
        feed_dict={
            tf_input: frame[None, ...]
            })

    boxes = boxes[0] # index by 0 to remove batch dimension
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]

    DETECTION_THRESHOLD = 0.5

    for i in range(int(num_detections)):
        if scores[i] < DETECTION_THRESHOLD:
            continue

        y_min = boxes[i][0]
        y_max = boxes[i][2]
        x_min = boxes[i][1]
        x_max = boxes[i][3]

        if DEBUG:
            print(f"Image: y_min={y_min}, y_max={y_max}, x_min={x_min}, x_max={x_max}")

        # scale box to image coordinates
        y_high_range = math.ceil(frame.shape[0] * y_max)
        y_low_range = math.floor(frame.shape[0] * y_min)
        y_height = y_high_range-y_low_range
        x_high_range = math.ceil(frame.shape[1] * x_max)
        x_low_range = math.floor(frame.shape[1] * x_min)
        x_width = x_high_range - x_low_range

        crop_faces = frame[ y_low_range:y_low_range+y_height,
                            x_low_range:x_low_range+x_width,
                            :]

        cv.imshow("crop", crop_faces)
        # Publish coordinates (debug)

        img_num+=1

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
