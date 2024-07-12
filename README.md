# camera-sense
AI Camera with scene understanding.

## Hardware Architecture
This application is based on the following hardware components:
* Raspberry Pi Zero 2 W (Wireless)
* Raspberry Pi Camera Module 3
* VEEKTOMX Mini Power Bank 10000mAh

## Software Architecture
The web server is based on FastAPI/Python3, while the client web application is based on Quasar/Vue/Node/Javascript. 
The web application allows the remote control of the camera to 
* Initial setup of 1 picture every 10s, looping
* Timelapse photography with custom defined interval, duration and naming
* Identification of Level indicators to analyse using April Tags (todo)
* Identification of areas to monitor for change (todo)
* Alerting the client app of Level Reached, Scene Change (todo)

## Instalation
A step-by-step tutorial for setting up a Raspberry Pi Zero W 2 computer as a vision system
* `sudo apt-get upgrade -y`
* `sudo apt-get install git -y`
* `sudo apt-get install cmake -y`
* `sudo apt-get install libssl-dev`
* `sudo apt-get install python3-pip -y`
* `sudo apt-get install python3-opencv`
* `pip install apriltag`
* `pip install fastapi`
* `pip install schedule`
* `pip install glob`

## Node installation
* `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`
* `nvm install 20`
* `npm i -g yarn@1`
* `yarn global add @quasar/cli`
* `yarn create quasar`

## Autostart by adding following to .bashrc
```
cd ~/projects/camera-sense


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

bash -c "make run-server"

```

## Troubleshooting
### Increase the size of iwatch
* `sudo nano /etc/sysctl.conf` and add line at bottom `fs.inotify.max_user_watches=524288`

### Increase the size of the Raspberry Pi Zero 2 swap space
```
sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=1024
```
