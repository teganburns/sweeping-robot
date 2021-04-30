cmake_minimum_required(VERSION 3.0.2)
project(imu)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roslaunch
  rospy
  rostest
  std_msgs
)

## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
catkin_python_setup()


################################################
## Declare ROS messages, services and actions ##
################################################

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
# LIBRARIES sensehat_ros
  CATKIN_DEPENDS rospy std_msgs
#  DEPENDS system_lib
)


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


#############
## Install ##
#############

#catkin_install_python(
#  PROGRAMS nodes/${PROJECT_NAME} 
#  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)
#
#install(DIRECTORY launch/
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
#  )
#
#install(DIRECTORY config/
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
#  )
#
##############
### Testing ##
##############
#
#if(CATKIN_ENABLE_TESTING)
#  find_package(rostest REQUIRED)
#  
#  catkin_add_nosetests(test/unit/test_library.py)
#
#  add_rostest(test/rostest/test_services.test)
#  add_rostest(test/rostest/test_publications.test)
#
#  roslaunch_add_file_check(launch)
#endif()

roslaunch_add_file_check(launch)
