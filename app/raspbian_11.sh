#!/bin/bash
sudo apt update -y
sudo apt install git python3 python3-dev python3-pip python3-venv libcurl4 software-properties-common openjdk-16-jdk-headless openjdk-16-jre-headless -y
sudo useradd crafty -s /bin/bash
