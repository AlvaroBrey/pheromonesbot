#!/usr/bin/env bash
pm2 stop pheromonesbot
git pull --ff
pip3 install --user -r requirements.txt
pm2 start pheromonesbot.py --interpreter python3
