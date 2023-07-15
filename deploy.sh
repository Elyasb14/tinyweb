#!/bin/bash

sudo apt update && sudo apt upgrade
sudo rm /etc/systemd/system/tinyweb.service
sudo rm /etc/nginx/sites-available/tinyweb
sudo rm /etc/nginx/sites-enabled/tinyweb

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

deactivate

touch tinyweb.ini

echo "
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = tinyweb.sock
chmod-socket = 660
vacuum = true

die-on-term = true
" >> tinyweb.ini

sudo touch /etc/systemd/system/tinyweb.service

sudo echo "
[Unit]
Description=uWSGI instance to serve tinyweb
After=network.target

[Service]
User=ebianchi
Group=www-data
WorkingDirectory=/home/ebianchi/tinyweb
Environment="PATH=/home/ebianchi/tinyweb/.venv/bin"
ExecStart=/home/ebianchi/tinyweb/.venv/bin/uwsgi --ini tinyweb.ini

[Install]
WantedBy=multi-user.target
" >> /etc/systemd/system/tinyweb.service

sudo chgrp www-data /home/ebianchi

sudo systemctl start tinyweb

sudo systemctl enable tinyweb

sudo touch /etc/nginx/sites-available/tinyweb

sudo echo "
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ebianchi/tinyweb/tinyweb.sock;
    }
}
" >> /etc/nginx/sites-available/tinyweb

sudo ln -s /etc/nginx/sites-available/tinyweb /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl restart nginx
