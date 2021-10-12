# sweeping-robot
1) Execute `./pull_repos.sh` to pull all the necessary repositories. (may need to `chmod +x pull_repos.sh`)
2) Execute `catkin_make_isolated --install --use-ninja`.
Build time takes 30-35 minutes on a Raspberry Pi 4B.
3) Source `source devel_isolated/setup.bash`
4) Execute `roslaunch imu imu.launch`
