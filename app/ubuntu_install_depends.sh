#!/bin/bash

#are we ready to install?
echo "We will now install Python 3.7, openjdk, git, and virtualenv"
echo "Type 1 for Yes - or - 2 for No then press enter"

#do we want to install software / upgrade system?
echo "Installing Required Software"
echo "Updating Apt"
sudo apt update -y
sudo apt install git python3.7 python3.7-dev python3-pip software-properties-common default-jre openjdk-8-jdk openjdk-8-jre-headless virtualenv -y

pip3 install virtualenv
