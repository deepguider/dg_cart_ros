#!/bin/bash

source /opt/ros/melodic/setup.bash
## Start roscore
pid=`pgrep roscore`
if [ ! -n "${pid}" ];then  # If process is not running.
    gnome-terminal --tab -- roscore
    sleep 2s    # wait until roscore is ready
fi

## Stop andro2linux_gps_rospublisher
pid=`pgrep andro2linux_gps_rospublisher`
if [ -n "${pid}" ];then  # If process is running.
    kill -9 ${pid}
fi
gnome-terminal --tab -- python2 andro2linux_gps_rospublisher.py

rostopic echo /andro2linux_gps
