#!/bin/bash

source /opt/ros/melodic/setup.bash
## Start roscore
pid=`pgrep roscore`
if [ ! -n "${pid}" ];then  # If process is not running.
    gnome-terminal --tab -- roscore
    sleep 2s    # wait until roscore is ready
fi

## Stop main_ros_python27
pid=`pgrep main_ros_python27`
if [ -n "${pid}" ];then  # If process is running.
    kill -9 ${pid}
fi
gnome-terminal --tab -- python2 main_ros_python27.py

pid=`pgrep image_view`
if [ -n "${pid}" ];then  # If process is running.
    kill -9 ${pid}
fi
rosrun image_view image_view image:=/theta360z1_raw  # for raw image
#rosrun image_view image_view image:=/theta360z1_compressed _image_transport:=compressed  # for compressed image
