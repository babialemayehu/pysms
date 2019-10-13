#! /bin/bash

sudo chmod -R a+rwx /dev/ttyUSB0
sudo chmod -R a+rwx /dev/ttyUSB1    
sudo chmod -R a+rwx /dev/ttyUSB2  

sudo systemctl stop ModemManager.service

sudo stty -F /dev/ttyUSB0 9600
sudo stty -F /dev/ttyUSB1 9600
sudo stty -F /dev/ttyUSB2 9600

# sudo cat < /dev/ttyUSB1

