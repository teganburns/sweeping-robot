#!/usr/bin/env bash

source /home/ubuntu/.bashrc
cd $SWEEPING_ROBOT_PATH
source devel_isolated/setup.bash
roslaunch sweeping_robot sensors.launch > /dev/null 2>&1



