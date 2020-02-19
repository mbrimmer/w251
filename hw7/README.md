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

This script will pull down a model from the web to be used in the .py file and then run the .py file.

## Questions
Describe your solution in detail. What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
> Solution is a mobilenet SSD(single shot multibox detector) based face detector with pretrained model provided, powered by tensorflow object detection api, trained by WIDERFACE dataset. I'm not sure the accuracy it achieves on labeled data, but it did very well with my face.<br>

Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
> It actually does pretty well. I wasn't giving the camera much variety aside from me in my computer chair, but it was capturing me from many angles that wasn't done from the OpenCV solution. I would probably not use it in a robust, production-grade system without knowing much more about it and doing some exhasutive testing, but it worked well for my purposes.

What framerate does this method achieve on the Jetson? Where is the bottleneck?
> 60fps. The bottleneck is probably with the processing / detection within the neural net.

Which is a better quality detector: the OpenCV or yours?
> Mine. It was capturing more images of me from various angles that OpenCv would never have captured and doing it at the needed speeds.
