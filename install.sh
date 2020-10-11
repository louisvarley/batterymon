#!/bin/bash

#get script path
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH


#if not root user, restart script as root
if [ "$(whoami)" != "root" ]; then
	echo "Switching to root user..."
	sudo bash $SCRIPT
	exit 1
fi

#set constants
IP="$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')"
NONE='\033[00m'
CYAN='\033[36m'
FUSCHIA='\033[35m'
UNDERLINE='\033[4m'

echo "Running Update..."

#install dependencies
sudo apt-get update
echo
echo "Installing Dependencies..."
echo

echo "Installing Python pip"
echo
sudo apt-get install python-pip
sudo apt-get install python3-pip

sudo pip3 install Adafruit_MCP3008
sudo pip3 install Adafruit_GPIO
sudo pip3 install configparser
sudo pip3 install re

sudo apt-get -y install python python-dev python-requests
sudo apt-get -y install sqlite3
sudo pip install flask flask-sqlalchemy flask-admin evdev
sudo pip install evdev --upgrade

echo "Cloning raspidmx"
echo
git clone https://github.com/AndrewFromMelbourne/raspidmx.git /tmp/raspidmx

echo "Building and installing raspidmx"
echo
cd tmp/raspidmx
make
cp /tmp/raspidmx/pngview/pngview /usr/local/bin
cd /home/pi/batterymon

rm -rf /tmp/rapsidmx

echo "Installing As Service"
echo 

#add batterymon.service to systemd
file1=$SCRIPTPATH"/batterymon.service"
cp $file1 /lib/systemd/system/
systemctl enable batterymon

echo "-----------------"
echo -e "${CYAN}Installation complete, ensure batterymon remains installed in /pi/home/batterymon/batterymon.py"
echo "-----------------"
