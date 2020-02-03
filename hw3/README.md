# Homework 3: Face Detection, Cropping, and Storage in Cloud
The objective of this is to build a lightweight IoT application pipeline with components running both on the edge (Nvidia Jetson TX2) and the cloud (a VM in Softlayer).

The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and - for now, just save these faces in the cloud for long term storage.

![Structure](https://raw.githubusercontent.com/mbrimmer/w251/master/hw3/StructureHW03.png)

## Part 1: Jetson TX2 (Container Config & VideoCapture)
1. Create Docker Images

docker build commands for ubuntu and alpine
```
docker build --network=host -t mosquitto_jtx2 -f DockerFile_mosquitto_tx2 .
docker build --network=host -t ubuntu_jtx2 -f DockerFile_ubuntu_tx2 .
```
Note: eliminating the need for --network=host is for future work as I was having trouble with messages getting outside of my localhost without this.

2. Create Local Network. Start Broker & Forwarder to send messages to public broker
Selected this methodology due to issues and time constraints in getting messaging directly to the cloud virtual server instance. Future enhancements to this code will focus on streamlining this.

```
# Create a bridge:
docker network create --driver bridge hw03

# Create an alpine linux - based mosquitto container:
docker run --name mosquitto --network hw03 -p :1883 -v "$PWD":/HW03 -d mosquitto_jtx2 sh -c "mosquitto -c /HW03/Jetson_Files/mqtt_broker_config.conf"

# Create an alpine linux - based message forwarder container:
docker run --name forwarder --network hw03 -v "$PWD":/HW03 -d mosquitto_jtx2 sh -c "mosquitto -c /HW03/Jetson_Files/mqtt_forwarder_config.conf"
```
The above code instantiates two containers. One to act as a broker and the other to act as a forwarder. The configuration files specify where the message will be routed. Right now, they are being routed from the broker to the forwarder and then to test.mosquitto.org.

3. Run image capture code
```
<from within /Jetson_Files>
./DockerFace
cd Jetson_Files
python3 faces_detect.py mosquitto
```
The above sets up an instance of the ubuntu_jtx2 image and leaves us at a bash shell where we can navigate to the Jetson_Files directory and kick off the python script that uses openCV to identify faces and commence the message passing.

Goal: At this point, screen shots are being made, cropped to just the face, and the face is being sent from the jetson ubuntu container, to a broker alpine container, to a forwarder alpine container, and to the public test.mosquitto.org server.

Credit Note: much of the code above and structure was based on office hours from Vinicio De Sola.

## Part 2: Cloud Virtual Server
1. Create Virtual server
We set this up in week 1/2 and are leveraging it for this assignment.
```
ibmcloud sl vs create ...
```
Then ensure that we are using public/private keys and passwords are turned off

2. Create Cloud Object Storage
Do this on the IBM cloud's web interface. <p>
My bucket name: **mbrimmer-faces-bucket**

3. Install Docker CE using Lab2 instructions

4. Install IBM Cloud Storage on VI
5. Add Cloud Storage
