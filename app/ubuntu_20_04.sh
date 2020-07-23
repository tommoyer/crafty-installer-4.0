#!/bin/bash
sudo apt update -y
sudo apt install git python3.8 python3.8-dev python3.8-venv python3-pip software-properties-common openjdk-8-jdk openjdk-8-jre virtualenv -y
pip3 install virtualenv
sudo useradd crafty