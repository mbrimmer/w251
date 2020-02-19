# Homework 7: Face Detection & Cropping Using Neural Network
This is a build off of HW3 where we used OpenCV to detect a face, crop the image, and then
send it to the cloud. In this homework, we are going to use a neural network to
detect the face instead of opencv. The rest could be the same.

### Note: I am focusing on the code to crop via neural network -- the rest could be re-added in if necessary

## Part 1: Jetson TX2 (Container Config & VideoCapture)
1. Build Docker Images

docker build commands - for jetson with Tensorflow, keras, opencv, etc.
```
docker build -t hw7_img -f Dockerfile.hw7 .
```

2. Create container
In order to instantiate the image we run the following from the /Jetson_files/ directory
```
./DockerFace_hw7.sh
```

The code it is running is the following: docker run --privileged --rm -p 8888:8888 -v "$PWD":/HW07 -it hw7_img bash

The above code instantiates a containers with keras, TF, OpenCV. We enter it with the bash command and navigate to /HW07/

3. Run image capture code
<from within container /HW07/>
```
./Run_Face_Detection.sh
```

This script will pull down a model from the web to be used in the .py file.
