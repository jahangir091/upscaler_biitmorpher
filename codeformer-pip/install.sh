#!/usr/bin/env bash
# clone the project first from github
# go to install.sh file
# chmod +x install.sh
# ./install.sh

python3 -m venv .venv
source .venv/bin/activate
pip instal .

# need to update install.sh
systemctl daemon-reload
systemctl start rembg
systemctl enable rembg
systemctl restart rembg

sudo cp upscaler_nginx.conf /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/upscaler_nginx.conf /etc/nginx/sites-enabled/


python main.py