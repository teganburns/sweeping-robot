#!/bin/bash
# This script downloads cartogropher cartographer_ros and rplidar repos.

# Variables
RPLIDAR_GIT='https://github.com/robopeak/rplidar_ros.git'
CARTOGRAPHER_GIT='https://github.com/cartographer-project/cartographer.git'
CARTOGRAPHER_ROS_GIT='https://github.com/cartographer-project/cartographer_ros.git'
ROS_ARDUINO_BRIDGE='https://github.com/teganburns/ROS_Arduino_bridge.git'
REPOS=( $RPLIDAR_GIT $CARTOGRAPHER_GIT $CARTOGRAPHER_ROS_GIT $ROS_ARDUINO_BRIDGE)
DIR='src/'

# Text Colors
CYAN='\033[0;36m' 
LG='\033[1;32m'
LR='\033[1;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

#Execution
echo -e "${WHITE}Moving to $DIR ${NC}"
cd $DIR

for repo in ${REPOS[@]}; do
    echo -e "${CYAN}Cloning $repo ${NC}"
    git clone $repo 
    echo -e "${LG}Success! $repo ${NC}"
done

echo -e "${WHITE}All repos cloned successfully!${NC}"
exit 0
