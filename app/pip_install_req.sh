#!/bin/bash
cd $1/crafty-web
git checkout $2

source ../venv/bin/activate

while true;do echo -n .;sleep 1;done &
pip3 install --no-cache-dir -r requirements.txt
kill $!; trap 'kill $!' SIGTERM
deactivate