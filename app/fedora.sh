#!/bin/bash
sudo dnf update -y
sudo dnf group install "Development tools" -y
sudo dnf install git python3 python3-devel java-1.8.0-openjdk java-1.8.0-openjdk-devel libffi libffi-devel -y
sudo useradd crafty -s /bin/bash
