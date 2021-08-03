#!/usr/bin/env bash

# check if the volume is initialized
if [ ! -d "/data/input" ]; then
    echo "/data/input folder does not exist, please finish the setup first!"
fi

# execute the rendering job
echo "execute the rendering job"
blender -b -P /main.py -- "$@"
