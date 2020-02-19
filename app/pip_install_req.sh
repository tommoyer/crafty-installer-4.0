#!/bin/bash
cd $1/crafty-web
git checkout $2

source ../venv/bin/activate

while :;do for s in / - \\ \|; do printf "\r$s";pip3 install --no-cache-dir -r requirements.txt;done;done

deactivate