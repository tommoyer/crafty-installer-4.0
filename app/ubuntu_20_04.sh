#!/bin/bash
sudo apt update -y
sudo apt install git python3 python3-dev python3-pip python3-venv libcurl4 software-properties-common -y
if [[ "$(uname -m)" == "aarch64" ]];then
	sudo apt install build-essential libssl-dev libffi-dev -y
fi
sudo useradd crafty -s /bin/bash
