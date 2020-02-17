#!/bin/bash
xhost + local:root
docker run \
--user=root \
--env="DISPLAY" \
--volume="/etc/group:/etc/group:ro" \
--volume="/etc/passwd:/etc/passwd:ro" \
--volume="/etc/shadow:/etc/shadow:ro" \
--volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
--name mb_face_app_hw7 --privileged --rm -p 8888:8888 -v "$PWD":/HW07 -it hw7_img bash
