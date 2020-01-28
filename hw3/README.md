# Homework 3: Face Detection, Cropping, and Storage in Cloud

## Part 1: Jetson TX2 (Container Config & VideoCapture)
1. Create Docker Images

```
docker build
docker build commands for ubuntu and alpine
```

2. Create Local Network / Run Broker & Forwarder

```
# Create a bridge:
docker network create --driver bridge hw03
# Create an alpine linux - based mosquitto container:
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh

# Create an alpine linux - based message forwarder container:
docker run --name forwarder --network hw03 -ti alpine sh
```

3. Run image capture code
```
python3 face_detect.py
```
## Part 2: Cloud Virtual Server
1. Create Virtual server
2. Create Cloud Object Storage
3. Install Docker CE using Lab2 instructions
4. Install IBM Cloud Storage on VI
5. Add Cloud Storage
