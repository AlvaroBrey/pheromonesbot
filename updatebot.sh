#!/usr/bin/env bash
pm2 stop pheromonesbot
git pull --ff
pip install --user -r requirements.txt
pm2 start pheromonesbot.py
