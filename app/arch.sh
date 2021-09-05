#!/bin/bash
sudo pacman -Syu
sudo pacman -S --noconfirm git extra/python extra/python-pip extra/jre16-openjdk extra/jdk16-openjdk
sudo useradd crafty -s /bin/bash
