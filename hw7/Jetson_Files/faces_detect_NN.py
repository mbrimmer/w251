"""""""""""""""""""""""""""""""""
Detect faces in USB video input and display
(will publish to mosquitto broker in future)

Calling method: python3 faces_video.py
"""""""""""""""""""""""""""""""""

import numpy as np
import cv2 as cv
import time
import sys
import math


DEBUG=True

#""""""""EVENTUALLY PULL THIS INTO Dockerfile"""""""""""
# https://github.com/yeephycho/tensorflow-face-detection
from PIL import Image
import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph

FROZEN_GRAPH_NAME='data/frozen_inference_graph_face.pb'
IMAGE_PATH='data/warriors.jpg'

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

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')

# image = Image.open(IMAGE_PATH)
#
# print('************************** IMAGE **************')
# plt.imshow(image)
# plt.show()
# print('************************** IMAGE **************')
#
# image_resized = np.array(image.resize((300, 300)))
# image = np.array(image)
#
# time.sleep(5)
#
# scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
#     tf_input: image_resized[None, ...]
# })
#
# boxes = boxes[0] # index by 0 to remove batch dimension
# scores = scores[0]
# classes = classes[0]
# num_detections = num_detections[0]
#
# # suppress boxes that are below the threshold..
# DETECTION_THRESHOLD = 0.5
#
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
#
# ax.imshow(image)
#
#
# # plot boxes exceeding score threshold
# for i in range(int(num_detections)):
#     if scores[i] < DETECTION_THRESHOLD:
#         continue
#     # scale box to image coordinates
#     box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
#
#     # display rectangle
#     patch = patches.Rectangle((box[1], box[0]), box[3] - box[1], box[2] - box[0], color='g', alpha=0.3)
#     ax.add_patch(patch)
#
#     # display class index and score
#     plt.text(x=box[1] + 10, y=box[2] - 10, s='%d (%0.2f) ' % (classes[i], scores[i]), color='w')
#
# plt.show()
#
# time.sleep(15)
#
# num_samples = 50
#
# t0 = time.time()
# for i in range(num_samples):
#     scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
#         tf_input: image_resized[None, ...]
#     })
# t1 = time.time()
# print('Average runtime: %f seconds' % (float(t1 - t0) / num_samples))
#
#
# time.sleep(30)

cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

img_num = 0


# Get Images
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

#    image_resized = np.array(frame.resize((300, 300)))

    #print('image_resized shape', image_resized.shape)
    img1 = cv.imshow('frame', frame)

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
        # box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])

        y_high_range = math.ceil(frame.shape[0] * y_max)
        y_low_range = math.floor(frame.shape[0] * y_min)
        y_height = y_high_range-y_low_range
        x_high_range = math.ceil(frame.shape[1] * x_max)
        x_low_range = math.floor(frame.shape[1] * x_min)
        x_width = x_high_range - x_low_range

        crop_faces = frame[ y_low_range:y_low_range+y_height,
                            x_low_range:x_low_range+x_width,
                            :]

        # frame[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        # Publish coordinates (debug)
        # coord_payload = str(img_num)+ ':' + ' (' + str(x) + "," + str(y) + ')'

        img_num+=1

    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
