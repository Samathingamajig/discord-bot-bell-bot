#!/bin/sh

TIMEOUT="5s"

while : ; do
  py -3 bell-bot.py
  echo "Restarting in $TIMEOUT"
  sleep $TIMEOUT
  echo ""
done