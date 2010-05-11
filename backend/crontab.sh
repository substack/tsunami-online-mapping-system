#!/bin/bash
# the script run by crontab

. $HOME/.profile
module load ncl-5.1.0
python monitor.py
