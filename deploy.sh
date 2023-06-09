#!/bin/bash

sudo apt update && sudo apt upgrade

python3 -m venv .venv
source .venv/bin/activate

pip install wheel 
pip install uwsgi flask
pip install -r requirements.txt

deactivate

sudo touch /etc/systemd/system/tinyweb.service

echo 

