# NoPresents 
My first attempt to set up Object Detection on my Raspberry Pi 5 with Google Coral USB Accelerator and the help of Docker. My goal with this project is to implement it with my cat flap and a servo motor to keep my cat from entering with prey in her mouth. Presents = Mice, Birds, Grasshoppers, Worms, Spiders ETC 🤮.
Part of the course "Building AI course project".

## Summary
I will try to set up object detection first, and train it to recognize when my cat has a prey in her mouth. When that works I will implement the servo motor as a "robot arm". It will keep the cat flap closed until my cat has proven she doesn't have a prey with her, then the "robot arm" will move and she can come in.

## Project specifications:
* Sure flap XL, cat flap with chip reader
* Raspberry 5 running Raspberry OS 64 bit
* Google Coral USB accelerator
* Iphone 14 pro max
* Servo motor
* Jumper cables
* Docker

## Step by step guide:
### PART ONE - SETTING UP THE RASPBERRY

1. DO A CLEAN INSTALL OF RASPBERRY PI OS (64-BIT) AND FLASH
IT ONTO A SD CARD WITH RASPBERRY PI IMAGER. ADD USER CREDENTIALS
AND WIFI NAME AND PASSWORD TO THE INSTALLATION FOR EASY ACCESS.

2. BOOT YOUR RASPBERRY AND USE YOUR COMPUTERS TERMINAL TO CONNECT VIA SSH: 
ssh tuff@pi.local
(username@raspberryname.local)

3. OPEN THE RASPI-CONFIG:
sudo raspi-config
GO TO INTERFACE OPTIONS AND ENABLE VNC CONNECTION.

4. RUN THE FOLLOWING COMMAND TO SEE THE RASPBERRYS IP ADDRESS:
ifconfig

5. DOWNLOAD VNC VIEWER TO YOUR COMPUTER AND CONNECT TO YOUR RASPBERRY:
username@ipaddress

6. INSTALL UPDATES AND IN THE TERMINAL RUN:
sudo apt update && sudo apt upgrade -y

7. REBOOT:
sudo reboot

### PART TWO - INSTALLING DOCKER

1. TO INSTALL DOCKER RUN:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

2. ADD YOUR USER TO THE DOCKER-GROUP
sudo usermod -aG docker $USER

3. REBOOT (IMPORTANT)
sudo reboot

4. VERIFY DOCKER INSTALLATION:
docker --version
YOU SHOULD GET SOMETHING LIKE 'Docker version 27.x.x' IN RETURN

5. INSTALL DOCKER COMPOSE TO MANAGE CONTAINERS:
sudo apt install -y docker-compose-plugin

6. VERIFY INSTALLATION:
docker compose version

7. CREATE A DIRECTORY FOR THIS PROJECT AND A DOCKERFILE TO SET UP 
PYTHON 3.9 AND CORAL DEPENDENCIES:
mkdir cod
cd cod
nano Dockerfile

8. COPY THE CODE IN THE 'Dockerfile' FROM MY REPO AND PASTE HERE, SAVE AND EXIT WITH: 'ctrl+o' -> enter -> 'ctrl+x'

9. BUILD THE DOCKER IMAGE:
docker build -t coral-object-detection .

### PART THREE - SET UP OBJECT DETECTION

1. IN THE DIRECTORY YOU CREATED (MINE IS 'cod') CREATE A NEW FILE:
nano object_detection.py

2. COPY THE CODE IN THE 'object_detection.py' FROM MY REPO AND PASTE HERE, SAVE AND EXIT WITH:
'ctrl+o' -> enter -> 'ctrl+x'
(NOTE: YOU HAVE TO CHANGE THE IP ADDRESS FROM THE ONE I'M USING, 10.0.1.16, TO YOUR IPHONES IPADDRESS. KEEP THE PORT :8081/video)!!!

3. INTO THE SAME DIRECTORY DOWNLOAD CORAL COMPATIBLE MODEL AND LABELS:
wget https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite
wget https://github.com/google-coral/test_data/raw/master/coco_labels.txt

4. CONNECT THE CORAL USB TO YOUR RASPBERRY, MAKE SURE TO USE ONE OF THE FASTER USB 3 PORTS
(BLUE)

5. DOWNLOAD THE DROIDCAM WEBCAM APP TO YOUR IPHONE

6. INSTALL VLC:
sudo apt install -y vlc

7. TEST THE CAMERA STREAM:
vlc http://10.0.1.16:8081/video

8. RUN THE DOCKER CONTAINER WITH:
docker run --name coral-objdet \
    --device=/dev/bus/usb:/dev/bus/usb \
    --network host \
    -v $(pwd):/app \
    coral-object-detection

9. INSTALL FEH WITH:
sudo apt install -y feh

10. RUN:
ls output_frame.jpg
feh output_frame.jpg

### PART FOUR - TRAINING MY OWN MODEL

## TO BE CONTINUED SOON
