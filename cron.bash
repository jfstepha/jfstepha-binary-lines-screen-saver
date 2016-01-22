#!/bin/bash
if pgrep -f ss.py ; then
    exit 0
else
    export DISPLAY=":0.0"
    /home/jfstepha/binaryLines/ss.py
fi
