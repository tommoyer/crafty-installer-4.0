#!/bin/bash
sudo pacman -Syu
sudo pacman -S --noconfirm git extra/python extra/python-pip extra/jre8-openjdk extra/jdk8-openjdk
sudo useradd crafty -s /bin/bash
