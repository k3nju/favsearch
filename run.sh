#! /usr/bin/bash

logger -p info -t tw "favcrawler booted"
source ./env/bin/activate
python ./favcrawler.py
logger -p info -t tw "favcrawler fin"

