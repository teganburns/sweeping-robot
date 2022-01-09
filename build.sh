#!/usr/bin/env bash

catkin_make_isolated --install --use-ninja
sudo chmod +x install_isolated/share/ros_arduino_python/nodes/arduino_node.py 
