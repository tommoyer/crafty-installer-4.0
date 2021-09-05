#!/bin/bash
sudo dnf update -y
sudo dnf group install "Development tools" -y
sudo dnf install git python3 python3-devel java-16-openjdk java-16-openjdk-devel -y
sudo useradd crafty -s /bin/bash
