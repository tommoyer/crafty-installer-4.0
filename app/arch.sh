#!/bin/bash
sudo pacman -Syu
sudo pacman -S --noconfirm git extra/python extra/python-pip extra/jre-openjdk extra/jdk-openjdk
sudo useradd crafty -s /bin/bash
