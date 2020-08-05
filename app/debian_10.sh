#!/bin/bash
sudo apt update -y
sudo apt install git python3 python3-dev python3-pip python3-venv software-properties-common openjdk-11-jdk openjdk-11-jre -y
sudo useradd crafty -s /bin/bash