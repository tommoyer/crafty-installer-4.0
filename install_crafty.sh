#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "Apologies - This script must be run as root"
   exit 1
else
  sudo apt install python3-pip -y
  pip3 install distro
  python3 install_crafty.py
fi

