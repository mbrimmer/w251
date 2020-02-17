# Homework 7: Face Detection & Cropping Using Neural Network
This is a build off of HW3 where we used OpenCV to detect a face, crop the image, and then
send it to the cloud. In this homework, we are going to use a neural network to
detect the face instead of opencv. The rest could be the same.

### Note: I am focusing on the code to crop via neural network -- the rest could be re-added in if necessary

## Part 1: Jetson TX2 (Container Config & VideoCapture)
1. Build Docker Images

docker build commands - for jetson with Tensorflow, keras, opencv, etc.
```
docker build
TBD
```
To

# Create an alpine linux - based message forwarder container:
docker run --name forwarder --network hw03 -v "$PWD"/..:/HW03 -d mosquitto_jtx2 sh -c "mosquitto -c /HW03/Jetson_Files/mqtt_forwarder_config.conf"
```
The above code instantiates two containers. One to act as a broker and the other to act as a forwarder. The configuration files specify where the message will be routed. Right now, they are being routed from the broker to the forwarder and then to test.mosquitto.org.

3. Run image capture code
```
<from within /Jetson_Files>
./DockerFace
cd /HW03/Jetson_Files
python3 faces_detect.py mosquitto
```
The above sets up an instance of the ubuntu_jtx2 image and leaves us at a bash shell where we can navigate to the Jetson_Files directory and kick off the python script that uses openCV to identify faces and commence the message passing.

Goal: At this point, screen shots are being made, cropped to just the face, and the face is being sent from the jetson ubuntu container, to a broker alpine container, to a forwarder alpine container, and to the public test.mosquitto.org server.

Credit Note: much of the code above and structure was based on office hours from Vinicio De Sola.
