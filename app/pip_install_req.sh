#!/bin/bash
cd $1/crafty-4
git checkout $2

source ../venv/bin/activate

pip3 install wheel
pip3 install setuptools==60.5.0
pip3 install --no-cache-dir -r requirements.txt
deactivate
