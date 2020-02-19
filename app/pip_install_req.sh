#!/bin/bash
cd $1
git checkout $2
source ./venv/bin/activate
pip3 install --no-cache-dir -r ./crafty-web/requirements.txt
deactivate