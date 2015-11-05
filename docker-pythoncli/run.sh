#!/bin/bash
stdbuf -oL /usr/sbin/python.py 2>&1 | /usr/bin/logger -d -n 172.17.42.1 -u /dev/null -t "$APP_LOGENTRIES_SET"