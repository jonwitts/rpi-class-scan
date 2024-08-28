#!/bin/bash

# Setup script for rpi-scan
# This script is part of https://github.com/queenmargarets/rpi-scan
# and will install the required Python libraries and SystemD
# service files for you

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./setup.sh"
  exit 1
fi

# update and upgrade existing packages
echo "Upgrading existing packages"
echo "=========================="
apt update && apt dist-upgrade -y && apt autoremove -y

# install our required packages
echo "Installing dependencies..."
echo "=========================="
apt install python3-dev python3-pip -y
pip3 install spidev --proxy http://10.0.96.1:800
pip3 install mfrc522 --proxy http://10.0.96.1:800
pip3 install python-tds --proxy http://10.0.96.1:800

# copy and activate our systemd definitions
echo "Copy and activate our systemd definition..."
echo "=========================="
cp ./rpi-scan.service /lib/systemd/system/rpi-scan.service
chmod 644 /lib/systemd/system/rpi-scan.service

# reload and enable
systemctl daemon-reload
systemctl enable rpi-scan.service

# Done
# exit the root shell
exit
