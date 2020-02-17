#!/bin/bash

mkdir data

FROZEN_GRAPH_NAME=data/frozen_inference_graph_face.pb
wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O "$FROZEN_GRAPH_NAME"

IMAGE_PATH=data/warriors.jpg
wget 'https://cdn.vox-cdn.com/thumbor/rC0mlBATZdoDW1tEa44P6431sGc=/0x0:3683x2455/1200x800/filters:focal(1623x234:2211x822)/cdn.vox-cdn.com/uploads/chorus_image/image/63273148/usa_today_12005182.0.jpg' -O "$IMAGE_PATH"


python3 faces_detect_NN.py
